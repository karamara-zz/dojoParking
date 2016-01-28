from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Vehicle, ParkingUser

class SignUpForm(UserCreationForm):
	username = forms.EmailField()
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
		)
	CHOICE_YEAR = (
		('', 'SELECT YEAR'),
		('2015','2015'),
		('2016','2016'),
		('2017','2017'),
		)
	cohortMonth = forms.ChoiceField( label = "Cohort Month", choices = CHOICE_MONTH, widget=forms.Select(attrs={'class':'browser-default'}))
	cohortYear = forms.ChoiceField( label = "Cohort", choices = CHOICE_YEAR, widget=forms.Select(attrs={'class':'browser-default'}))
	class Meta:
		model = User
		fields = ('username', 'cohortMonth', 'cohortYear', 'password1', 'password2')
	def save(self, commit=True):
		user = super(SignUpForm, self).save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		cohortdata = self.cleaned_data['cohortMonth']
		print self.cleaned_data['cohortMonth']
		if commit:
			print "committed and saving user"
			user.save()
			print cohortdata, "cohortMonth"
			parkingUser = ParkingUser.objects.create(cohort = "aug", user = user)
			return user
class SearchForm(forms.Form):
	plate_number = forms.CharField(label = "Licence Plate Number ", max_length = 10, widget=forms.TextInput(attrs={'class':'capital'}))
class VehicleForm(ModelForm):
	class Meta:
		model = Vehicle
		fields = ['make','model','plate_number','color']
