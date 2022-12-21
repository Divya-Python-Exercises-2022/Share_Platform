from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from platform_user.models import PlatformUser, Address
from platform_user.serializers import AddressSerializer
from products.models import Products
from products.serializers import ProductSerializer


class MyProductAPIViewSet(LoginRequiredMixin, APIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        platform_user = PlatformUser.objects.filter(django_user_id=self.request.user.id)
        products = Products.objects.filter(shared_user_id=platform_user[0].id)

        address = Address.objects.filter(platform_user_id=platform_user[0].id)

        serializer1 = ProductSerializer(products, many=True)

        serializer2 = AddressSerializer(address, many=True)

        #return Response(({"Products": ProductSerializer(products[i]).data} for i in range(0, len(products))), status=201)
        return Response(serializer1.data)

    def post(self, request, *args, **kwargs):
        platform_user = PlatformUser.objects.filter(django_user_id=self.request.user.id)
        #products = Products.objects.filter(shared_user_id=platform_user[0].id)
        address = Address.objects.filter(platform_user_id=platform_user[0].id)

        serializer1 = ProductSerializer(data=request.data)
        #serializer2 = AddressSerializer(address, data=request.data)

        print(f'Filtered address:{address}')
        if serializer1.is_valid():
            name = serializer1.data['name']
            about = serializer1.data['about']
            pick_up_date = serializer1.data['pick_up_date']
            pick_up_place = serializer1.data['pick_up_place']
            pick_up_time = serializer1.data['pick_up_time']
            quantity = serializer1.data['quantity']
            status_of_availability = serializer1.data['status_of_availability']

            with transaction.atomic():
                print(pick_up_place)
                platform_user = PlatformUser.objects.filter(django_user_id=self.request.user.id)
                products = Products.objects.create(name=name, about=about, pick_up_date=pick_up_date,pick_up_time=pick_up_time,
                                                   pick_up_place_id=pick_up_place, quantity=quantity,
                                                   status_of_availability=status_of_availability,
                                                   shared_user_id=platform_user[0].id)

                return Response({"Products added": ProductSerializer(products).data}, status=201)
        return Response({"Error: invalid data, could not create the client"}, status=400)

class AllProductAPIViewSet(LoginRequiredMixin, APIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

    def get(self, request):
        product = Products.objects.all()
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data)

