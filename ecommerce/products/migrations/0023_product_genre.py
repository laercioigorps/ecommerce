# Generated by Django 4.0.8 on 2022-11-29 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0022_product_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='genre',
            field=models.CharField(choices=[('G', 'Girl')], max_length=20, null=True),
        ),
    ]
