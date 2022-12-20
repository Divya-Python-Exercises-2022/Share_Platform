from django.db import models

from platform_user.models import PlatformUser, Address

class Products(models.Model):
    shared_user = models.ForeignKey(PlatformUser, on_delete=models.CASCADE, related_name='my_product', null=True)
    name = models.CharField(max_length=200)
    about = models.CharField(max_length=200)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_place = models.ForeignKey(Address, blank=True, on_delete=models.CASCADE, related_name='related_products') # Same address can have multiple products
    quantity = models.PositiveIntegerField()
    status_of_availability = models.BooleanField()

    def __str__(self):
        return f'{self.name}-{self.about}"\n"{self.pick_up_date}-{self.pick_up_time}"\n"{self.pick_up_place}'