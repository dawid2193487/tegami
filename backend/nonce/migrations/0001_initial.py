# Generated by Django 3.0.3 on 2020-03-22 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Nonce',
            fields=[
                ('value', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
