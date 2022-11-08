from django.db import models

from platform_user.models import PlatformUser, Address


# Create your models here.
class Products(models.Model):
    shared_user = models.ForeignKey(PlatformUser, on_delete=models.CASCADE, related_name='my_product', null=True)
    name = models.CharField(max_length=200)
    about = models.CharField(max_length=200)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_place = models.OneToOneField(Address, blank=True, on_delete=models.CASCADE)  # Todo implement maps
