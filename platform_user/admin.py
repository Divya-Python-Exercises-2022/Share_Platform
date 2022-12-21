from django.contrib import admin

from platform_user.models import PlatformUser, Address

# Register your models here.
admin.site.register(PlatformUser)
admin.site.register(Address)