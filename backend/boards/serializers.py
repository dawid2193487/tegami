from rest_framework import serializers
from .models import Reply, Thread, Board

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['pk', 'name', 'description', 'slug', 'created_at']

class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = ['pk', 'posted_by', 'message', 'board', 'posted_at']

class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ['pk', 'posted_by', 'message', 'reply_in', 'posted_at']
