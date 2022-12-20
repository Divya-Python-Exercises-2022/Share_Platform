from rest_framework import serializers

from platform_user.models import PlatformUser, Address
from products.serializers import ProductSerializer


class PlatformUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformUser
        exclude = ['django_user']

class AddressSerializer(serializers.ModelSerializer):
    related_products = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = Address
        exclude = ['platform_user']
