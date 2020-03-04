from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ('name', )}
    readonly_fields = ('created_on',)

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    readonly_fields = ('posted_on',)

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    readonly_fields = ('posted_on',)
