# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django import forms

# --------------------------------------------------------------
# App imports
# --------------------------------------------------------------
from core.models import Contact


class ContactForm(forms.ModelForm):
    '''
    Basic model-form for our contact model
    '''

    name = forms.CharField(max_length=100, required=True,
		widget=forms.TextInput(attrs={
			'placeholder': 'Full name',
			'class': 'form-control'}))

    email = forms.EmailField(max_length=255, required=True,
		widget=forms.EmailInput(attrs={
			'placeholder': 'Email address',
			'class': 'form-control'}))

    message = forms.CharField(max_length=1000, required=False,
      widget=forms.Textarea(attrs={
        'placeholder': 'Message'}))

    class Meta:
        model = Contact
        fields = ('name', 'email', 'message')