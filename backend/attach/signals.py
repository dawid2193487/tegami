from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Attachment
from .tasks import create_thumb

@receiver(post_save, sender=Attachment)
def make_thumb(sender, instance, created, **kwargs):
    if created:
        create_thumb(instance)

