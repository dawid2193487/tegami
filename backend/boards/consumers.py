from channels.generic.websocket import JsonWebsocketConsumer
from channels.exceptions import StopConsumer
from .models import Thread
from django.forms.models import model_to_dict
from asgiref.sync import async_to_sync

class ThreadConsumer(JsonWebsocketConsumer):

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
        
    def receive_json(self, content):
        pass

    def new_reply(self, event):
        self.send_json({
            "type": "new_reply",
            "reply": event["reply"]
        })

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(self.chan_id, self.channel_name)
        raise StopConsumer
