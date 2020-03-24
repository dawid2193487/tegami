from rest_framework import serializers
from .models import Attachment

class AttachmentSerializer(serializers.Serializer):
    path = serializers.SerializerMethodField('get_upload')
    thumb = serializers.SerializerMethodField('get_thumb')
    name = serializers.SerializerMethodField('get_name')
    class Meta:
        model = Attachment
        fields = ['path']

    def get_upload(self, obj):
        return obj.upload.url
    
    def get_thumb(self, obj):
        if obj.thumbnail:
            return obj.thumbnail.url
        else:
            return None
    
    def get_name(self, obj):
        return obj.upload.name