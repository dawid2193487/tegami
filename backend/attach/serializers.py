from rest_framework import serializers
from .models import Attachment

class AttachmentSerializer(serializers.Serializer):
    path = serializers.SerializerMethodField('get_upload')
    name = serializers.SerializerMethodField('get_name')
    class Meta:
        model = Attachment
        fields = ['path']

    def get_upload(self, obj):
        return obj.upload.url
    
    def get_name(self, obj):
        return obj.upload.name