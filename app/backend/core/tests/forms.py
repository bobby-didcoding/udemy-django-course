# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django.test import TestCase

# --------------------------------------------------------------
# App Party imports
# --------------------------------------------------------------
from core.forms import (
    ContactForm,
    GenericNewsLetterForm,
)

class ContactFormTestCase(TestCase):
    """
    Test suite for ContactForm
    """

    def setUp(self):
        
        self.form_data = {
            "name": "Bobby Stearman",
            "email": "test@case.com",
            "message": "This is a test message"
        }

    def test_contact_form_expected_form_submission(self):
        form_data = self.form_data
        form = ContactForm(data=form_data)
        
        self.assertTrue(form.is_valid())


class GenericNewsLetterFormTestCase(TestCase):
    """
    Test suite for GenericNewsLetterForm
    """

    def setUp(self):
        
        self.form_data = {
            "nl_email": "test@case.com",
        }

    def test_generic_newsletter_form_expected_form_submission(self):
        form_data = self.form_data
        form = GenericNewsLetterForm(data=form_data)
        
        self.assertTrue(form.is_valid())
