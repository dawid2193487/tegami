# Generated by Django 3.0.3 on 2020-03-01 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0005_board_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='slug',
            field=models.SlugField(default='a', max_length=20),
            preserve_default=False,
        ),
    ]
