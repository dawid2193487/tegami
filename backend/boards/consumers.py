from django.forms.models import model_to_dict
from django.contrib.auth import get_user_model
from channels.generic.websocket import JsonWebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync

from .models import Thread, Reply, Board
from .serializers import ThreadSerializer, ReplySerializer, BoardSerializer
from profiles.serializers import ProfileSerializer
from nonce.models import Nonce

class InvalidParameters(Exception):
    pass

class AccessConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.watched_thread = None
        self.watched_board = None
        self.accept()

    def receive_json(self, content):
        t = content["type"]
        # without the "tegami_" prefix below, this could be exploited as an RCE
        func = getattr(self, f'tegami_{t}', None)
        if func is None:
            self.send_json({
                "type": "no_such_call",
                "nonce": content["nonce"],
                "call_copy": content
            })
            return

        try:
            response = func(content)
            response["nonce"] = content["nonce"]
            self.send_json(response)
        except (InvalidParameters, KeyError):
            self.send_json({
                "type": "invalid_call",
                "nonce": content["nonce"],
                "call_copy": content
            })

    @staticmethod
    def tegami_board_list(content):
        boards = Board.objects.all()
        return {
            "type": "board_list",
            "boards": BoardSerializer(boards, many=True).data,
        }

    @staticmethod
    def tegami_board_detail(content):
        board = Board.objects.get(pk=content["pk"])
        return {
            "type": "board_detail",
            "board": BoardSerializer(board).data,
        }
    
    @staticmethod
    def tegami_thread_list(content):
        board = Board.objects.get(pk=content["pk"])
        threads = ThreadSerializer(board.thread_set.all(), many=True).data
        return {
            "type": "thread_list",
            "board": BoardSerializer(board).data,
            "threads": threads,
        }

    @staticmethod
    def tegami_thread_detail(content):
        thread = Thread.objects.get(pk=content["pk"])
        return {
            "type": "thread_detail",
            "thread": ThreadSerializer(thread).data,
        }

    def tegami_watch_thread(self, content):
        thread = Thread.objects.get(pk=content["pk"])
        if self.watched_thread is not None:
            async_to_sync(self.channel_layer.group_discard)(self.watched_thread, self.channel_name)
        self.watched_thread = thread.channel_id
        async_to_sync(self.channel_layer.group_add)(self.watched_thread, self.channel_name)
        return {
            "type": "thread_watched_ok",
            "thread": content["pk"],
        }

    def tegami_watch_board(self, content):
        thread = Board.objects.get(pk=content["pk"])
        if self.watched_board is not None:
            async_to_sync(self.channel_layer.group_discard)(self.watched_board, self.channel_name)
        self.watched_board = thread.channel_id
        async_to_sync(self.channel_layer.group_add)(self.watched_board, self.channel_name)
        return {
            "type": "board_watched_ok",
            "board": content["pk"]
        }

    @staticmethod
    def tegami_reply_list(content):
        thread = Thread.objects.get(pk=content["pk"])
        replies = ReplySerializer(thread.reply_set.all(), many=True).data
        return {
            "type": "reply_list",
            "thread": ThreadSerializer(thread).data,
            "replies": replies,
        }

    @staticmethod
    def tegami_reply_detail(content):
        reply = Reply.objects.get(pk=content["pk"])
        return {
            "type": "reply_detail",
            "reply": ReplySerializer(reply).data,
        }

    @staticmethod
    def tegami_profile_detail(content):
        user = get_user_model().objects.get(pk=content["pk"])
        profile = user.profile
        return {
            "type": "profile_detail",
            "profile": ProfileSerializer(profile).data,
        }

    def tegami_post_reply(self, content):
        Nonce.check_used(content["nonce"])
        thread = Thread.objects.get(pk=content["pk"])
        reply = Reply.objects.create(
            posted_by=self.scope["user"],
            message=content["message"],
            reply_in=thread
        )
        print("posted")
        Nonce.stamp(content["nonce"])
        return {
            "type": "post_reply_ok",
        }

    def broadcast_thread(self, event):
        thread_message = AccessConsumer.tegami_thread_detail({"pk": event["pk"]})
        self.send_json(thread_message)

    def broadcast_board(self, event):
        board_message = AccessConsumer.tegami_board_detail({"pk": event["pk"]})
        self.send_json(board_message)


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
