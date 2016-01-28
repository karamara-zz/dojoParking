from django.contrib import admin

# Register your models here.
from .models import ParkingUser, Vehicle
admin.site.register(ParkingUser)
admin.site.register(Vehicle)