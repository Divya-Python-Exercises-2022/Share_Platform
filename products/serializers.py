
from rest_framework import serializers

from products.models import Products


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['name', 'about','pick_up_date','pick_up_time','pick_up_place','quantity','status_of_availability']
