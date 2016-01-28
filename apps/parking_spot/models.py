from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
class ParkingUser(models.Model):
	user = models.OneToOneField(User, on_delete= models.CASCADE)
	cohort = models.CharField(max_length = 20)
	def __str__(self):
		return self.user.username
	class Meta:
		db_table= "pakring user"
# Create your models here.
class Vehicle(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE, default = 1)
	make = models.CharField(max_length = 20)
	model = models.CharField(max_length = 20)
	color = models.CharField(max_length = 10)
	plate_number = models.CharField(max_length = 10)
	def __str__(self):
		return self.make
	class Meta:
		db_table = 'vehicles'


