# Generated by Django 4.0.8 on 2023-02-05 17:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0008_delete_shoppingcartpage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=7)),
                ('shipping', models.DecimalField(decimal_places=2, max_digits=6)),
                ('total', models.DecimalField(decimal_places=2, max_digits=7)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('CT', 'CREATED')], default='CT', max_length=2)),
                ('shipping_address', models.CharField(max_length=150)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.shoppingcart')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
