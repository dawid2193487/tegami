# Generated by Django 3.0.3 on 2020-03-01 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='description',
            field=models.CharField(default='', max_length=255, verbose_name='Description'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='board',
            name='name',
            field=models.CharField(max_length=20, verbose_name='Name'),
        ),
    ]
