# Generated by Django 4.0.8 on 2022-11-30 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0027_product_usage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='url',
            field=models.CharField(max_length=200),
        ),
    ]
