from rest_framework import serializers

from platform_user.models import PlatformUser, Address


class PlatformUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformUser
        exclude = ['django_user']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ['platform_user']
