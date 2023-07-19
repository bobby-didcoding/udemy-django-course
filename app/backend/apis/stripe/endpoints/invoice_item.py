# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django.conf import settings
from django.utils.decorators import method_decorator
from django.test.utils import override_settings

# --------------------------------------------------------------
# 3rd party imports
# --------------------------------------------------------------
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

class InvoiceItem:
    '''
    This handles all API calls to Stripes Invoice Item endpoint
    '''
    def __init__(self, invoice_item):
        self.invoice_item = invoice_item
        self.external_id = invoice_item.external_id

    
    def get(self):
        '''
        Docs - https://stripe.com/docs/api/invoiceitems/retrieve?lang=python
        '''
        obj = stripe.InvoiceItem.retrieve(
            self.external_id,
            )
        return obj


    def put(self):
        '''
        Docs - https://stripe.com/docs/api/invoiceitems/modify?lang=python
        '''
        obj = stripe.InvoiceItem.modify(
            self.external_id,
            )
        return obj

    @method_decorator(override_settings(SUSPEND_SIGNALS=True))
    def post(self):
        '''
        Docs - https://stripe.com/docs/api/invoiceitems/create?lang=python
        '''
        obj = stripe.InvoiceItem.create(
            customer= self.external_id(),
            unit_amount= self.invoice_item.unit_amount(),
            quantity = self.invoice_item.quantity,
            currency=self.invoice_item.amount.currency.lower(),
            description= self.invoice_item.title,
            )
        return obj

