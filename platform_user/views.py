from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from django.db import transaction

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
