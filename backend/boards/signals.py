from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms.models import model_to_dict

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Reply
from .serializers import ThreadSerializer, ReplySerializer
from .consumers import AccessConsumer

@receiver(post_save, sender=Reply)
def reply_broadcast(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    
    thread_chan_id = instance.reply_in.channel_id
    async_to_sync(channel_layer.group_send)(thread_chan_id, {
        "type": "broadcast_thread",
        "pk": instance.reply_in.pk
    })
    print(f"sent thread update to {thread_chan_id}");

    print("sending board update");
    board_chan_id = instance.reply_in.board.channel_id
    async_to_sync(channel_layer.group_send)(board_chan_id, {
        "type": "broadcast_board",
        "pk": instance.reply_in.board.pk
    })
