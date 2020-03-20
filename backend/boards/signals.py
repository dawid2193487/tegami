from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms.models import model_to_dict

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Reply
from .serializers import ThreadSerializer, ReplySerializer

@receiver(post_save, sender=Reply)
def reply_broadcast(sender, instance, **kwargs):
    chan_id = instance.reply_in.channel_id
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(chan_id, {
        "type": "new_reply",
        "reply": ReplySerializer(instance).data, 
    })
