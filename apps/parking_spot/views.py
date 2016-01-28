from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import SearchForm, SignUpForm, VehicleForm
from .models import Vehicle
from django.contrib.auth import forms, login, logout, authenticate
# Create your views here.
class Index(View):
	def get(self, request):
		return render(request, 'parking_spot/search.html', {'SearchForm': SearchForm})
class SignUp(View):
	form = SignUpForm
	def get(self, request):
		return render(request, 'parking_spot/create.html', {'SignUpForm' : self.form})
	def post(self, request):
		print "post request to sign up"
		signUp = self.form(request.POST)
		if signUp.is_valid():
			user = self.form(request.POST).save()
		else:
			print "not valid"
			context = {'SignUpForm': signUp}
			return render(request, 'parking_spot/create.html', context)
		return redirect('/')
class SignIn(View):
	form = forms.AuthenticationForm
	def get(self, request):
		return render(request, 'parking_spot/login.html', {'form': self.form})
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
				return render(request, 'parking_spot/login.html', {'form': form})
		else:
			return render(request, 'parking_spot/login.html', {'form': form})
		return redirect('/')
class User(View):
	form = VehicleForm
	def get(self, request, id):
		print id, request.user.id
		if int(id) == int(request.user.id):
			try:
				v = Vehicle.objects.get(owner = id)
			except:
				pass
			return render(request, 'parking_spot/user.html', {'form' : self.form})
		else:
			return redirect('/')
	def post(self,request):
		print request.POST
		form = self.form(request.POST or None)
		print form
		if form.is_valid():
			form.owner = request.user
			form.save()
			print "saved"
		else:
			print "form is not valid"
			return render(request, 'parking_spot/user.html', {'form': form})