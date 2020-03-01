from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    pass

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    pass