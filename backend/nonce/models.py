from django.db import models

# Create your models here.
class Nonce(models.Model):
    value = models.UUIDField(primary_key=True, editable=False)
    time = models.DateTimeField(auto_now_add=True)
