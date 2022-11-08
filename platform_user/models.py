from django.db import models

# Create your models here.
class PlatformUser(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField()
    phone = models.CharField(max_length=20)


class Address(models.Model):
    street = models.CharField(max_length=100)
    number = models.IntegerField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip = models.CharField(max_length=20)
    platform_user = models.ForeignKey(PlatformUser, on_delete=models.CASCADE)

