from django.db import models
from django.conf import settings

# Create your models here.
class Profile(models.Model):
    display_name = models.CharField(max_length=48)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, models.CASCADE)