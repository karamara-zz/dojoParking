from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import View
from .forms import SearchForm, SignUpForm, VehicleForm, SignInForm
from .models import Vehicle, BlackList, Warnings, ParkingUser
from django.contrib.auth import forms, login, logout, authenticate
from django.core import serializers
import json
# Create your views here.
class Index(View):
	form = SearchForm
	def get(self, request):
		return render(request, 'parking_spot/search.html', {'SearchForm': self.form, 'title':'Search'})
	def post(self, request):
		form = self.form(request.POST or None)
		content = {'SearchForm':form, 'title':'Search'}
		plate = request.POST['plate_number']
		if form.is_valid():
			try:
				v = Vehicle.objects.get(plate_number__iexact = plate)
				parkingUser = ParkingUser.objects.get(user = v.owner)
				content['is_staff'] = parkingUser.is_staff
				return render(request, 'parking_spot/success.html', content)
			except:
				BL = BlackList.objects.filter(plate_number__iexact = plate)
				if len(BL) > 0:
					warnings = Warnings.objects.filter(black_list = BL)
					print warnings
					content['warnings'] = warnings
				content['plate_number'] = plate
				return render(request, 'parking_spot/fail.html', content)
class Warning(View):
	def post(self, request):
		plate = request.POST['plate_number']
		print int(request.POST['warning_given'])
		try:
			BL = BlackList.objects.get(plate_number = plate)
			print "warning is given before"
		except:
			BL = BlackList.objects.create(plate_number = plate)
		warn = Warnings.objects.create(black_list = BL, reported_by = request.user)
		BL.save()
		warn.save()
		print warn
		return redirect('/')
class SignUp(View):
	form = SignUpForm
	def get(self, request):
		return render(request, 'parking_spot/create.html', {'SignUpForm' : self.form , 'title':'Sign up'})
	def post(self, request):
		print "post request to sign up"
		signUp = self.form(request.POST)
		if signUp.is_valid():
			user = self.form(request.POST).save()
		else:
			context = {'SignUpForm': signUp , 'title':'Sign up'}
			return render(request, 'parking_spot/create.html', context)
		return redirect('/')
class SignIn(View):
	form = SignInForm
	def get(self, request):
		return render(request, 'parking_spot/login.html', {'form': self.form , 'title':'Sign In'})
	def post(self,request):
		form = self.form(None, request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username = username, password = password)
			if user is not None:
				login(request, user)
				return redirect('/user/{}'.format(user.id))
			else:
				return render(request, 'parking_spot/login.html', {'form': form, 'title':'Sign In'})
		else:
			return render(request, 'parking_spot/login.html', {'form': form, 'title':'Sign In'})
		return redirect('/')
class Search(View):
	form = SearchForm
	def get(self, request, input_plate):
		print input_plate
		v = Vehicle.objects.filter(plate_number__iexact = input_plate)
		data = serializers.serialize("json", v)
		data = json.loads(data)
		return JsonResponse(data, safe=False)
class User(View):
	form = VehicleForm
	def get(self, request, id):
		content = {'form': self.form, 'title':'User Detail'}
		if int(id) == int(request.user.id):
			try:
				v = Vehicle.objects.filter(owner=request.user)
				content['vehicles'] = v
			except:
				pass
			return render(request, 'parking_spot/user.html', content)
		else:
			return redirect('/')
	def post(self,request):
		form = self.form(request.POST or None)
		content = {'form': form , 'title':'User Detail'}
		if form.is_valid():
			print "saved", form
			form.save(request.user)
			return redirect('/user/'+str(request.user.id))
		else:
			print request.user
			try:
				v = Vehicle.objects.filter(owner=request.user)
				content['vehicles'] = v
			except:
				pass
			return render(request, 'parking_spot/user.html', content)
class Delete(View):
	def post(self, request):
		vehicle = int(request.POST['vehicle'])
		print vehicle
		v = Vehicle.objects.get(id = vehicle)
		v.delete()
		return redirect('/user/'+str(request.user.id))
class Logout(View):
	def get(self,request):
		logout(request)
		return redirect('/')