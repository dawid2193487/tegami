from rest_framework import serializers
from django.db.models import Prefetch

from .models import Reply, Thread, Board
from attach.serializers import AttachmentSerializer

class BoardSerializer(serializers.ModelSerializer):
    #queryset = Board.objects.prefetch_related(Prefetch("thread_set", queryset=Thread.objects.order_by("posted_at")))
    #thread_set = serializers.PrimaryKeyRelatedField(many=True, queryset=Thread.objects.all().order_by("pk"))
    class Meta:
        model = Board
        fields = ['pk', 'name', 'description', 'slug', 'color', 'created_at']

class ThreadSerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(many=True)
    class Meta:
        model = Thread
        fields = ['pk', 'posted_by', 'message', 'board', 'posted_at', 'reply_set', 'attachments']

class ReplySerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(many=True)
    class Meta:
        model = Reply
        fields = ['pk', 'posted_by', 'message', 'reply_in', 'posted_at', 'attachments']
