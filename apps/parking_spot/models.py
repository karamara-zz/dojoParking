from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
class ParkingUser(models.Model):
	user = models.OneToOneField(User, on_delete= models.CASCADE)
	cohort = models.DateField(max_length = 20)
	is_staff = models.BooleanField(default = False)
	updated_at = models.DateField(auto_now = True)
	created_at = models.DateField(default = timezone.now)
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
	created_at = models.DateField(default = timezone.now)
	checked_at = models.DateField(auto_now= True)
	def __str__(self):
		return self.make
	class Meta:
		db_table = 'vehicles'
class BlackList(models.Model):
	plate_number = models.CharField(max_length=10)
	created_at = models.DateField(default = timezone.now)
	updated_at = models.DateField(auto_now = True)
	def __str__(self):
		return self.plate_number
	class Meta:
		db_table = 'black list'
class Warnings(models.Model):
	black_list = models.ForeignKey(BlackList, on_delete= models.CASCADE)
	reported_by = models.ForeignKey(User, on_delete= models.CASCADE)
	created_at = models.DateField(auto_now = True)
	def __str__(self):
		return str(self.black_list) +" at "+str(self.created_at)


