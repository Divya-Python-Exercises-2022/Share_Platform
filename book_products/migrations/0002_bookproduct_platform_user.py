# Generated by Django 4.1.2 on 2022-12-11 19:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('platform_user', '0006_alter_address_platform_user'),
        ('book_products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookproduct',
            name='platform_user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='platform_user.platformuser'),
            preserve_default=False,
        ),
    ]
