# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django.conf import settings


# --------------------------------------------------------------
# 3rd party imports
# --------------------------------------------------------------
import requests



def reCAPTCHAValidation(token):

	''' reCAPTCHA validation '''
	result = requests.post(
		'https://www.google.com/recaptcha/api/siteverify',
		 data={
		 	'secret': settings.RECAPTCHA_PRIVATE_KEY,
			'response': token
		 })

	return result.json()


def FormErrors(*args):
	'''
	Handles form error that are passed back to AJAX calls
	'''
	message = ""
	for f in args:
		if f.errors:
			message = f.errors.as_text()
	return message

