from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    readonly_fields = ("thumbnail",)