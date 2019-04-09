from django import forms
from django.forms import ModelForm
from user.models import User
from django.contrib.auth.forms import AuthenticationForm


class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta():
		model = User
		fields = ('name','username','password','email','gender','address')

	def save(self, *args, **kwargs):
		user = super(UserForm, self).save(commit=False, *args, **kwargs)
		user.is_active = True 
		user.save()
		return user

class LoginForm(AuthenticationForm):
	username=forms.CharField(max_length=50)
	password = forms.CharField(widget=forms.PasswordInput())
