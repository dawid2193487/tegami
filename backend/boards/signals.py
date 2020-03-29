from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.forms.models import model_to_dict

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Reply, Thread
from .serializers import ThreadSerializer, ReplySerializer
from .consumers import AccessConsumer

@receiver(post_save, sender=Reply)
def reply_broadcast(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    
    board_chan_id = instance.reply_in.board.channel_id
    async_to_sync(channel_layer.group_send)(board_chan_id, {
        "type": "broadcast_board",
        "pk": instance.reply_in.board.pk
    })
    
    thread_chan_id = instance.reply_in.channel_id
    async_to_sync(channel_layer.group_send)(thread_chan_id, {
        "type": "broadcast_thread",
        "pk": instance.reply_in.pk
    })
    async_to_sync(channel_layer.group_send)(board_chan_id, {
        "type": "broadcast_thread",
        "pk": instance.reply_in.pk
    })


@receiver(post_save, sender=Thread)
def thread_broadcast(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    
    board_chan_id = instance.board.channel_id
    async_to_sync(channel_layer.group_send)(board_chan_id, {
        "type": "broadcast_board",
        "pk": instance.board.pk
    })
    async_to_sync(channel_layer.group_send)(board_chan_id, {
        "type": "broadcast_thread",
        "pk": instance.pk
    })

@receiver(pre_save, sender=Reply)
def bump(sender, instance, **kwargs):
    from datetime import datetime
    instance.reply_in.bump_at = datetime.now()
    instance.reply_in.save()