from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from django.db import transaction
from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView

from platform_user.models import PlatformUser, Address
from platform_user.serializers import PlatformUserSerializer, AddressSerializer


# No login required for registration
class PlatformUserAPIViewSet(APIView):
    queryset = PlatformUser.objects.all()
    serializer_class = PlatformUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = PlatformUserSerializer(data=request.data)
        if serializer.is_valid():
            first_name = serializer.data['first_name']
            last_name = serializer.data['last_name']
            email = serializer.data['email']
            password = serializer.data['password']
            phone = serializer.data['phone']

            with transaction.atomic():
                django_user = User.objects.create_user(username=email, email=email, password=password)
                platform_user = PlatformUser.objects.create(first_name=first_name, last_name=last_name,email=email,password=password, phone=phone, django_user=django_user)

                return Response({"Platform User created": PlatformUserSerializer(platform_user).data}, status=201)
        return Response({"Error: invalid data, could not create the client"}, status=400)

class PlatformUserDetailsAPIView(LoginRequiredMixin, APIView):
    queryset = PlatformUser.objects.all()
    serializer_class = PlatformUserSerializer

    def get(self, request, *args, **kwargs):
        user = PlatformUser.objects.filter(django_user_id=self.request.user.id)
        serializer = PlatformUserSerializer(user[0])
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        user = self.get(request)
        serializer = PlatformUserSerializer(user, data=request.data)

        if serializer.is_valid():
            first_name = serializer.validated_data['first_name']
            last_name = serializer.validated_data['last_name']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            phone = serializer.validated_data['phone']
            with transaction.atomic():
                PlatformUser.objects.filter(django_user_id=self.request.user.id).update(first_name=first_name, last_name=last_name, email=email, password=password,
                                                             phone=phone)
                User.objects.filter(id=self.request.user.id).update(username=email, email=email, password=make_password(password))
                return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response('Invalid data')


class AddressAPIViewSet(LoginRequiredMixin, APIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def get(self, request, *args, **kwargs):
        platform_user = PlatformUser.objects.filter(django_user_id=self.request.user.id)  # request.session.get('platform_user_id'))
        address = Address.objects.filter(platform_user_id=platform_user[0].id)

        return Response(({"Addresses": AddressSerializer(address[i]).data} for i in range(0, len(address))), status=201)

    def post(self, request, *args, **kwargs):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            street = serializer.data['street']
            number = serializer.data['number']
            city = serializer.data['city']
            country = serializer.data['country']
            zip = serializer.data['zip']

            with transaction.atomic():
                platform_user = PlatformUser.objects.filter(django_user_id=self.request.user.id)
                address = Address.objects.create(street=street, number=number, city=city,
                                                            country=country, zip=zip, platform_user_id=platform_user[0].id)

                return Response({"Address added": AddressSerializer(address).data}, status=201)
        return Response({"Error: invalid data, could not create the client"}, status=400)

class AddressDetailsAPIView(LoginRequiredMixin, APIView):
    def get(self, request, address_id):
        try:
            platform_user = PlatformUser.objects.filter(django_user_id=self.request.user.id)
            address = Address.objects.get(id=address_id, platform_user_id=platform_user[0].id)
            serializer = AddressSerializer(address)
            return Response(serializer.data)
        except Address.DoesNotExist:
            return Response(status=404)

    def delete(self, request, address_id):
            Address.objects.filter(id=address_id).delete()
            return Response(status=200)

    def put(self, request, address_id):
        address = self.get(request, address_id)
        serializer = AddressSerializer(address, data=request.data)
        if serializer.is_valid():
            street = serializer.validated_data['street']
            number = serializer.validated_data['number']
            city = serializer.validated_data['city']
            country = serializer.validated_data['country']
            zip = serializer.validated_data['zip']
            Address.objects.filter(id=address_id).update(street=street, number=number, city=city, country=country, zip=zip)
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response('Invalid data')
