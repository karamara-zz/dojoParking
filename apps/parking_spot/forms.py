from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Vehicle, ParkingUser
import datetime, re
from django.core.exceptions import ValidationError
class SignInForm(AuthenticationForm):
	username = forms.EmailField(label = "email")
class SignUpForm(UserCreationForm):
	username = forms.EmailField(label="E-mail")
	CHOICE_MONTH = (
		('','SELECT MONTH'),
		('01', 'January'),
		('02', 'Febuary'),
		('03', 'March'),
		('04', 'April'),
		('05', 'May'),
		('06', 'June'),
		('07', 'July'),
		('08', 'August'),
		('09', 'September'),
		('10', 'October'),
		('11', 'November'),
		('12', 'December'),
		('12', 'STAFF'),
		)
	CHOICE_YEAR = (
		('', 'SELECT YEAR'),
		('2015','2015'),
		('2016','2016'),
		('2017','2017'),
		('2018','2018'),
		('2050','STAFF'),
		)
	cohortMonth = forms.ChoiceField( label = "Cohort Month", choices = CHOICE_MONTH, widget=forms.Select(attrs={'class':'browser-default'}))
	cohortYear = forms.ChoiceField( label = "Cohort Year", choices = CHOICE_YEAR, widget=forms.Select(attrs={'class':'browser-default'}))
	class Meta:
		model = User
		fields = ('username','first_name','last_name', 'cohortMonth', 'cohortYear', 'password1', 'password2')
	def save(self, commit=True):
		user = super(SignUpForm, self).save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		cohort_date = self.cleaned_data['cohortMonth']+"-"+self.cleaned_data['cohortYear']
		cohort_date = datetime.datetime.strptime(cohort_date, "%m-%Y")

		print self.cleaned_data['cohortMonth']
		if commit:
			print "committed and saving user"
			user.save()
			is_staff = False
			if re.match(r'^.+@codingdojo.com$', self.cleaned_data['username']):
				is_staff = True
			print cohort_date, "cohortMonth"
			parkingUser = ParkingUser.objects.create(cohort = cohort_date, user = user, is_staff = is_staff)
			return user
class SearchForm(forms.Form):
	plate_number = forms.CharField(label = "Licence Plate Number ", max_length = 10, widget=forms.TextInput(attrs={'class':'capital'}))
class VehicleForm(ModelForm):
	def clean_plate_number(self):
		plate_number = self.cleaned_data['plate_number']
		if Vehicle.objects.filter(plate_number__iexact=plate_number).exists():
			raise ValidationError("plate number already exists")
		return plate_number
	class Meta:
		model = Vehicle
		fields = ['make','model','plate_number','color']
	def save(self, owner, commit = True):
		user = super(VehicleForm, self).save(commit = False)
		user.owner = owner
		if commit:
			user.save()
			return user
