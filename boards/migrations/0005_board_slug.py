# Generated by Django 3.0.3 on 2020-03-01 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0004_auto_20200301_1915'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='slug',
            field=models.SlugField(default='a', max_length=20),
            preserve_default=False,
        ),
    ]