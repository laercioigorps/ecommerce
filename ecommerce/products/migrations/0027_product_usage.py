# Generated by Django 4.0.8 on 2022-11-29 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0026_alter_product_genre'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='usage',
            field=models.CharField(default=None, max_length=30),
            preserve_default=False,
        ),
    ]
