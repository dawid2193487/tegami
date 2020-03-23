from django.db import models

# Create your models here.
class Nonce(models.Model):
    value = models.UUIDField(primary_key=True, editable=False)
    time = models.DateTimeField(auto_now_add=True)

    @classmethod
    def check_used(cls, nonce):
        return cls.objects.filter(value=nonce).exists()

    @classmethod
    def stamp(cls, nonce):
        cls.objects.create(value=nonce)
