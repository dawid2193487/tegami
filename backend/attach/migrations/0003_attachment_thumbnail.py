# Generated by Django 3.0.3 on 2020-03-24 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attach', '0002_auto_20200323_2047'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachment',
            name='thumbnail',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]
