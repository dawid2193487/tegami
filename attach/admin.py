from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Attachement)
class AttachementAdmin(admin.ModelAdmin):
    pass