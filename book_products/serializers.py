
from rest_framework import serializers

from book_products.models import BookProduct


class BookProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookProduct
        exclude = ['platform_user']
