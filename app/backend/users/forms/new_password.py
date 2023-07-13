# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django import forms
from django.contrib.auth.forms import  SetPasswordForm
from django.contrib.auth import get_user_model

User = get_user_model()

class NewPasswordForm(SetPasswordForm):
	'''
	Form that uses built-in SetPasswordForm to handel resetting passwords
	'''
	recaptcha_token = forms.CharField(
        widget=forms.HiddenInput())
	
	new_password1 = forms.CharField(
		widget=forms.PasswordInput(attrs={'placeholder': '*Password..','class':'password form-control'}))
	new_password2 = forms.CharField(
		widget=forms.PasswordInput(attrs={'placeholder': '*Confirm Password..','class':'password form-control'}))

	class Meta:
		model = User
		fields = ('password1', 'password2', )