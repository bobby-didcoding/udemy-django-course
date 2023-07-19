# --------------------------------------------------------------
# Python imports
# --------------------------------------------------------------
from dateutil.relativedelta import *
from datetime import datetime
from django.utils.decorators import method_decorator
from django.test.utils import override_settings

# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django.conf import settings

# --------------------------------------------------------------
# 3rd party imports
# --------------------------------------------------------------
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

class Invoice:
    '''
    This handles all API calls to Stripes Invoice endpoint
    '''
    def __init__(self, customer, **kwargs):
        self.customer = customer
        self.external_id = customer.external_id
        self.invoice = kwargs.get("invoice")
        if self.invoice:
            self.invoice_external_id = self.invoice.external_id


    def all(self):
        '''
        Docs - https://stripe.com/docs/api/invoices/list?lang=python
        '''
        obj = stripe.Invoice.list(
            self.external_id,
            )
        return obj


    def serializer(self, invoice):
        invoice_info = {
                    "invoice_id": invoice["id"], 
                    "invoice_url": invoice["hosted_invoice_url"], 
                    "invoice_pdf": invoice["invoice_pdf"], 
                    "invoice_description": invoice["lines"]["data"][0]["description"],
                    "invoice_total": invoice["amount_paid"]/100,
                    "invoice_paid": invoice["paid"],
                    "invoice_date": datetime.fromtimestamp(int(invoice["created"])).strftime('%d-%m-%Y'),
                    }
        return invoice_info


    def get(self):
        '''
        Docs - https://stripe.com/docs/api/invoices/retreive?lang=python
        '''
        obj = stripe.Invoice.retrieve(
            self.invoice_external_id,
            )
        return obj
    
    def get_upcoming(self):
        '''
        Docs - https://stripe.com/docs/api/invoices/retreive?lang=python
        '''
        obj = stripe.Invoice.upcoming(
            customer=self.external_id,
            )
        self.subscription.upcoming_amount = obj["total"]
        self.subscription.save()
        return obj
    

    def put(self, method, invoice_id, **kwargs):
        '''
        Docs - https://stripe.com/docs/api/invoices/finalize?lang=python
        Docs - https://stripe.com/docs/api/invoices/pay?lang=python
        '''
        source_id = kwargs.get("source_id")
        match method:
            case 'finalize':
                invoice = stripe.Invoice.finalize_invoice(invoice_id,stripe_account=self.account_external_id)
            case 'pay':
                invoice = stripe.Invoice.pay(invoice_id,source=source_id, stripe_account=self.account_external_id)
        return invoice

    @method_decorator(override_settings(SUSPEND_SIGNALS=True))
    def post(self):
        '''
        Docs - https://stripe.com/docs/api/invoices/create?lang=python
        '''
        cart = self.cart_object()
        amount = cart.amount

        if self.token:
            source = self.post_source()
            self.source_id = source["id"]
        
        #create invoice items
        items = []
        for item in cart.items.all():
            items.append(self.post_invoice_item(item))
        
        #created invoice items will automatically be added to this invoice
        new_invoice = stripe.Invoice.create(
            customer=self.external_id,
            collection_method="charge_automatically",
        )

        #manually finalize the invoice before making a payment request
        invoice = self.put_invoice('finalize', new_invoice.id)

        try:
            self.put_invoice('pay', invoice.id, source_id = self.source_id)
            invoice = self.invoice_object(invoice.id, items, self.source_id)

            #Now create non stock items
            for item in items:
                self.item_object(item)

            
        except stripe.error.CardError as e:
            message = "Card Error"
            status = "500"
            return {"status": status, "message": message}

        except stripe.error.RateLimitError as e:
            message = "Rate limit error"
            status = "500"
            return {"status": status, "message": message}
        
        except stripe.error.InvalidRequestError as e:
            message = "Invalid parameter"
            status = "500"
            return {"status": status, "message": message}
        
        except stripe.error.AuthenticationError as e:
            message = "Not authenticated"
            status = "500"
            return {"status": status, "message": message}

        except stripe.error.APIConnectionError as e:
            message = "Network error"
            status = "500"
            return {"status": status, "message": message}
        
        except stripe.error.StripeError as e:
            message = "Something went wrong, you were not charged"
            status = "500"
            return {"status": status, "message": message}
        
        except Exception as e:
            message = "Serious error, we have been notified"
            status = "500"
            return {"status": status, "message": message}

        #clear carts
        CartItem.objects.clear_items(self.user)
        
        message = "Success! Your payment was successful"
        status = "200"
        return {"status": status, "message": message, "id":invoice.id}
