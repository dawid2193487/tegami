from django.db import models
from django.utils.text import slugify 
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from attach.models import Attachement

# Create your models here.
class Board(models.Model):
    name = models.CharField(verbose_name="Name", max_length=20)
    description = models.CharField(verbose_name="Description", max_length=255)
    slug = models.SlugField(max_length=20)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Thread(models.Model):
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    message = models.TextField(verbose_name="Message", max_length=6000)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    posted_on = models.DateTimeField(auto_now_add=True)
    attachements = GenericRelation(Attachement)

    def __str__(self):
        return f'{self.board.name} » {self.message[:100]}'

class Reply(models.Model):
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    message = models.TextField(verbose_name="Message", max_length=6000)
    reply_in = models.ForeignKey(Thread, on_delete=models.CASCADE)
    posted_on = models.DateTimeField(auto_now_add=True)
    attachements = GenericRelation(Attachement)

    class Meta:
        verbose_name_plural = "Replies"

    def __str__(self):
        return f'{self.reply_in.board.name} » {self.reply_in.message[:30]} » {self.message[:100]}'