from django.forms.models import model_to_dict
from django.contrib.auth import get_user_model
from channels.generic.websocket import JsonWebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync

from .models import Thread

class InvalidParameters(Exception):
    pass

class AccessConsumer(JsonWebsocketConsumer):
    def receive_json(self, content):
        t = content["type"]
        # without the "tegami_" prefix below, this could be exploited as an RCE
        func = getattr(self, f'tegami_{t}', None)
        if func is None:
            self.send_json({
                "type": "no_such_call",
                "call_copy": content
            })
            return

        try:
            func(content)
        except (InvalidParameters, KeyError):
            self.send_json({
                "type": "invalid_call",
                "call_copy": content
            })

    def tegami_get_profile(self, content):
        user = get_user_model().objects.get(pk=content["pk"])
        profile = user.profile
        self.send_json({
            "type": "profile_detail",
            "profile": model_to_dict(profile),
        })

class ThreadConsumer(AccessConsumer):

    def connect(self):
        self.accept()
        thread = Thread.objects.get(pk=self.scope["url_route"]["kwargs"]["thread_id"])
        replies = [ model_to_dict(reply) for reply in thread.reply_set.all() ]
        self.chan_id = thread.channel_id
        async_to_sync(self.channel_layer.group_add)(self.chan_id, self.channel_name)

        self.send_json({
            "type": "thread_init",
            "thread": model_to_dict(thread),
            "replies": replies
        })

    def new_reply(self, event):
        self.send_json({
            "type": "new_reply",
            "reply": event["reply"]
        })

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(self.chan_id, self.channel_name)
        self.send_json({
            "type": "disconnect",
        })
        raise StopConsumer
