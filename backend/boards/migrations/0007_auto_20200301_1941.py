# Generated by Django 3.0.3 on 2020-03-01 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0006_thread_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='slug',
            field=models.SlugField(max_length=80),
        ),
    ]
