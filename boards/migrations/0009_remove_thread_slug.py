# Generated by Django 3.0.3 on 2020-03-01 19:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0008_auto_20200301_1941'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thread',
            name='slug',
        ),
    ]
