from django.contrib.auth.models import User
from django.db import models
from rest_framework import request

from django.http import request
class PlatformUser(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    django_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='platform_user')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Address(models.Model):
    street = models.CharField(max_length=100)
    number = models.IntegerField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip = models.CharField(max_length=20)
    platform_user = models.ForeignKey(PlatformUser, on_delete=models.CASCADE, related_name='related_address') # One user can have many addresses


    def __str__(self):
        return f'{self.street}-{self.number}-{self.city}'