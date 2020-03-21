from django.forms.models import model_to_dict
from django.contrib.auth import get_user_model
from channels.generic.websocket import JsonWebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync

from .models import Thread, Reply, Board
from .serializers import ThreadSerializer, ReplySerializer, BoardSerializer
from profiles.serializers import ProfileSerializer

class InvalidParameters(Exception):
    pass

class AccessConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.watched_thread = None
        self.accept()

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

    def tegami_board_list(self, content):
        boards = Board.objects.all()
        self.send_json({
            "type": "board_list",
            "boards": BoardSerializer(boards, many=True).data,
        })

    def tegami_board_detail(self, content):
        board = Board.objects.get(pk=content["pk"])
        self.send_json({
            "type": "board_detail",
            "board": BoardSerializer(board).data,
        })
    
    def tegami_thread_list(self, content):
        board = Board.objects.get(pk=content["pk"])
        threads = ThreadSerializer(board.thread_set.all(), many=True).data
        self.send_json({
            "type": "thread_list",
            "board": BoardSerializer(board).data,
            "threads": threads,
        })

    def tegami_thread_detail(self, content):
        thread = Thread.objects.get(pk=content["pk"])
        self.send_json({
            "type": "thread_detail",
            "thread": ThreadSerializer(thread).data,
        })

    def tegami_watch_thread(self, content):
        thread = Thread.objects.get(pk=content["pk"])
        if self.watched_thread is not None:
            async_to_sync(self.channel_layer.group_discard)(self.watched_thread, self.channel_name)
        self.watched_thread = thread.channel_id
        async_to_sync(self.channel_layer.group_add)(self.watched_thread, self.channel_name)

    def tegami_reply_list(self, content):
        thread = Thread.objects.get(pk=content["pk"])
        replies = ReplySerializer(thread.reply_set.all(), many=True).data
        self.send_json({
            "type": "reply_list",
            "replies": replies,
        })

    def tegami_profile_detail(self, content):
        user = get_user_model().objects.get(pk=content["pk"])
        profile = user.profile
        self.send_json({
            "type": "profile_detail",
            "profile": ProfileSerializer(profile).data,
        })
    # def tegami_unwatch_thread(self, content):
    #     thread = Thread.objects.get(pk=content["pk"])
    #     self.chan_id = thread.channel_id
    #     async_to_sync(self.channel_layer.group_discard)(self.chan_id, self.channel_name)

# class ThreadConsumer(AccessConsumer):

#     def connect(self):
#         self.accept()
#         thread = Thread.objects.get(pk=self.scope["url_route"]["kwargs"]["thread_id"])
#         replies = ReplySerializer(thread.reply_set.all(), many=True).data
#         self.chan_id = thread.channel_id
#         async_to_sync(self.channel_layer.group_add)(self.chan_id, self.channel_name)

#         self.send_json({
#             "type": "thread_init",
#             "thread": ThreadSerializer(thread).data,
#             "replies": replies
#         })

#     def new_reply(self, event):
#         self.send_json({
#             "type": "new_reply",
#             "reply": event["reply"]
#         })

#     def disconnect(self, code):
#         async_to_sync(self.channel_layer.group_discard)(self.chan_id, self.channel_name)
#         self.send_json({
#             "type": "disconnect",
#         })
#         raise StopConsumer
