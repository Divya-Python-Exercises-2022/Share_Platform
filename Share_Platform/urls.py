"""Share_Platform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from book_products.views import BookProductAPIViewSet, BookProductDetailsAPIViewSet
from platform_user.views import PlatformUserAPIViewSet, AddressAPIViewSet, AddressDetailsAPIView, \
    PlatformUserDetailsAPIView  # , LoginAPIViewSet
from products.views import MyProductAPIViewSet, AllProductAPIViewSet
router = DefaultRouter()
#router.register(r'register',PlatformUserAPIViewSet)
#router.register(r'add_addresses',AddressAPIViewSet)
#router.register(r'login', LoginAPIViewSet)

urlpatterns = [
    path('api-auth',include('rest_framework.urls')),
    #path('api/v1/',include(router.urls)),
    path('register/',PlatformUserAPIViewSet.as_view()),
    path('my_details/',PlatformUserDetailsAPIView.as_view()),
    path('my_addresses/', AddressAPIViewSet.as_view()),
    path('my_addresses/<int:address_id>',AddressDetailsAPIView.as_view()),
    path('my_products/',MyProductAPIViewSet.as_view()),
    path('list_all_products/', AllProductAPIViewSet.as_view()),
    path('book_products/',BookProductAPIViewSet.as_view()),
    path('book_products/<int:booking_id>',BookProductDetailsAPIViewSet.as_view()),
    #path('login/', LoginAPIViewSet.as_view()),
    path('admin/', admin.site.urls),
]
