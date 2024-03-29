# Generated by Django 4.1.2 on 2022-11-20 10:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('platform_user', '0006_alter_address_platform_user'),
        ('products', '0002_products_quantity_products_status_of_availability'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='pick_up_place',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_products', to='platform_user.address'),
        ),
    ]
