from rest_framework import serializers
from .models import Reply, Thread, Board

class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ['pk', 'posted_by', 'message', 'reply_in', 'posted_at']

class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = ['pk', 'posted_by', 'message', 'board', 'posted_at']