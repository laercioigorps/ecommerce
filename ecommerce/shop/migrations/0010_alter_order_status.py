# Generated by Django 4.0.8 on 2023-02-05 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('CREATED', 'Created')], default='CREATED', max_length=20),
        ),
    ]
