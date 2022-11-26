# Generated by Django 4.0.8 on 2022-11-26 09:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_size_created_at_size_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='colour',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2022, 11, 26, 9, 16, 14, 409783)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='colour',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]