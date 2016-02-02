from django.contrib import admin

# Register your models here.
from .models import ParkingUser, Vehicle, BlackList, Warnings
admin.site.register(ParkingUser)
admin.site.register(Vehicle)
admin.site.register(BlackList)
admin.site.register(Warnings)