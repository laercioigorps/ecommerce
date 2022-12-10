# Generated by Django 4.0.8 on 2022-11-29 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0024_alter_product_genre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='genre',
            field=models.CharField(choices=[('G', 'Girl'), ('B', 'Boys'), ('W', 'Women')], max_length=20, null=True),
        ),
    ]