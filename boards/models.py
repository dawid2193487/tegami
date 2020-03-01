from django.db import models

# Create your models here.
class Board(models.Model):
    name = models.CharField(verbose_name="Name", max_length=20)
    description = models.CharField(verbose_name="Description", max_length=255)

    def __str__(self):
        return self.name

class Thread(models.Model):
    message = models.TextField(verbose_name="Message", max_length=6000)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)

    def __str__(self):
        return self.message[:100]