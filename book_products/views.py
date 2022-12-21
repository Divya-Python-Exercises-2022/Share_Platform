from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from book_products.models import BookProduct
from book_products.serializers import BookProductSerializer
from products.models import Products


class BookProductAPIViewSet(LoginRequiredMixin, APIView):
    queryset = BookProduct.objects.all()
    serializer_class = BookProductSerializer

    def get(self, request, *args, **kwargs):
        booked_products = BookProduct.objects.filter(platform_user_id = self.request.user.id)
        serializer = BookProductSerializer(booked_products, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = BookProductSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            pick_up_address = serializer.data['address']
            pick_up_product = serializer.data['product']

            hasproduct = Products.objects.filter(id=pick_up_product, pick_up_place_id = pick_up_address)
            if hasproduct:
                quantity = hasproduct[0].quantity
                if quantity > 0:
                    with transaction.atomic():
                        booked_product = BookProduct.objects.create(address_id=pick_up_address, product_id=pick_up_product, platform_user_id=self.request.user.id)
                        if hasproduct[0].quantity == 1:
                            hasproduct.update(status_of_availability=False, quantity=hasproduct[0].quantity - 1)
                        elif hasproduct[0].quantity > 1:
                            Products.objects.get(id=pick_up_product, pick_up_place_id = pick_up_address).update(quantity=hasproduct[0].quantity - 1)
                        return Response(BookProductSerializer(booked_product).data, status=201)
        return Response('Product is not available', status=400)


class BookProductDetailsAPIViewSet(LoginRequiredMixin, APIView):
    queryset = BookProduct.objects.all()
    serializer_class = BookProductSerializer

    def get(self, request, booking_id):
        try:
            booked_products = BookProduct.objects.get(id=booking_id)
            serializer = BookProductSerializer(booked_products)
            return Response(serializer.data)
        except BookProduct.DoesNotExist:
            return Response(status=404)

    def delete(self, request, booking_id):
        booked_Product = self.get(request, booking_id=booking_id)
        serializer = BookProductSerializer(booked_Product, data=request.data)

        print((booked_Product.data)['product'])
        booked_product = Products.objects.filter(id=(booked_Product.data)['product'], pick_up_place_id=(booked_Product.data)['address'])
        BookProduct.objects.filter(id=booking_id).delete()
        if booked_product[0].quantity == 0:
            booked_product.update(status_of_availability=True, quantity=booked_product[0].quantity + 1)
        elif booked_product[0].quantity >= 1:
            Products.objects.get(id=(booked_Product.data)['product'], pick_up_place_id=(booked_Product.data)['address']).update(
                quantity=booked_product[0].quantity + 1)
        return Response('Booking Deleted', status=200)


    def put(self, request, booking_id): #todo Update the previously chosen product with its availability and quantity
        booked_Product = self.get(request, booking_id=booking_id)
        serializer = BookProductSerializer(booked_Product, data=request.data)

        if serializer.is_valid():

            pick_up_address = serializer.validated_data['address']
            pick_up_product = serializer.validated_data['product']

            hasproduct = Products.objects.filter(id=pick_up_product.id, pick_up_place_id=pick_up_address.id)
            if hasproduct:
                quantity = hasproduct[0].quantity
                if quantity > 0:
                    with transaction.atomic():
                        BookProduct.objects.filter(id=booking_id).update(address_id=pick_up_address.id,
                                                                         product_id=pick_up_product.id)
                        if hasproduct[0].quantity == 1:
                            hasproduct.update(status_of_availability=False, quantity=hasproduct[0].quantity - 1)
                        elif hasproduct[0].quantity > 1:
                            Products.objects.get(id=pick_up_product.id, pick_up_place_id=pick_up_address.id).update(
                                quantity=hasproduct[0].quantity - 1)
                        return Response('Booking updated', status=status.HTTP_200_OK)
        return Response('Product is not available', status=400)