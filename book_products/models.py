from django.db import models

from platform_user.models import Address, PlatformUser
from products.models import Products


# Create your models here.
class BookProduct(models.Model):
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='Choose product with the related address')
    platform_user = models.ForeignKey(PlatformUser, on_delete=models.CASCADE)
