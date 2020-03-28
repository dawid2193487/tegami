from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
import uuid

# Create your models here.
class Attachment(models.Model):
    upload = models.FileField()
    thumbnail = models.FileField(null=True)
    upload_token = models.UUIDField(default=uuid.uuid4, editable=False)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        indexes = [
            models.Index(fields=("upload_token", ))
        ]

    def __str__(self):
        return f'{str(self.upload)} ∈ {str(self.content_object)}'