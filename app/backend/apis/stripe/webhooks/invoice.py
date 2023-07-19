# --------------------------------------------------------------
# Python imports
# --------------------------------------------------------------
import logging

# --------------------------------------------------------------
# Project imports
# --------------------------------------------------------------
from ecommerce.models import Invoice, Customer, InvoiceItem, Price

# --------------------------------------------------------------
# App imports
# --------------------------------------------------------------
from apis.stripe import print_webhook_event, convert_naive_to_aware


logger = logging.getLogger(__name__)


class InvoiceWebhook:
    """
    {
        'id': 'in_1Mb0fQPBB3lIVWh6qpHNokN9', 
        'object': 'invoice', 
        'account_country': 'GB', 
        'account_name': 'Didcoding', 
        'account_tax_ids': None, 
        'amount_due': 0, 
        'amount_paid': 0, 
        'amount_remaining': 0, 
        'amount_shipping': 0, 
        'application': 'ca_NJoXuLv1nZsiRTfFF8CqmXq8aireAorE', 
        'application_fee_amount': 0, 
        'attempt_count': 0, 
        'attempted': True, 
        'auto_advance': False, 
        'automatic_tax': {
            'enabled': False, 
            'status': None
        }, 
        'billing_reason': 'subscription_create', 
        'charge': None, 
        'collection_method': 'charge_automatically', 
        'created': 1676289476, 
        'currency': 'gbp', 
        'custom_fields': None, 
        'customer': 'cus_NLi5DY2ptQTQkX', 
        'customer_address': None, 
        'customer_email': 'bobby+3@didcoding.com', 
        'customer_name': 'Bobby3 Stearman', 
        'customer_phone': None, 
        'customer_shipping': None, 
        'customer_tax_exempt': 'none', 
        'customer_tax_ids': [], 
        'default_payment_method': None, 
        'default_source': None, 
        'default_tax_rates': [], 
        'description': None, 
        'discount': {
            'id': 'di_1Mb0fQPBB3lIVWh65IiMhkkb', 
            'object': 'discount', 
            'checkout_session': None, 
            'coupon': {
                'id': 'jlUhIacf', 
                'object': 'coupon', 
                'amount_off': None, 
                'created': 1676280441, 
                'currency': None, 
                'duration': 'forever', 
                'duration_in_months': None, 
                'livemode': False, 
                'max_redemptions': None, 
                'metadata': {
                    'internal_id': '7b00b571-3436-4463-8864-cf2489b5eb19'
                }, 
                'name': 'Multi Event/Squaddy discount - 33%', 
                'percent_off': 33.0, 
                'redeem_by': None, 
                'times_redeemed': 2, 
                'valid': True
            }, 
            'customer': 'cus_NLi5DY2ptQTQkX', 
            'end': None, 
            'invoice': None, 
            'invoice_item': None, 
            'promotion_code': None, 
            'start': 1676289476, 
            'subscription': 'sub_1Mb0fQPBB3lIVWh6i0W5DIer'
        }, 
        'discounts': ['di_1Mb0fQPBB3lIVWh65IiMhkkb'], 
        'due_date': None, 
        'ending_balance': 0, 
        'footer': None, 
        'from_invoice': None, 
        'hosted_invoice_url': 'https://invoice.stripe.com/i/acct_1MZC2YPBB3lIVWh6/test_YWNjdF8xTVpDMllQQkIzbElWV2g2LF9OTGk1WWpYQjBrQnNOUjlUYXNsYjNqcjJIWjBXS2R1LDY2ODMwMjc30200LTh4PI6G?s=ap', 
        'invoice_pdf': 'https://pay.stripe.com/invoice/acct_1MZC2YPBB3lIVWh6/test_YWNjdF8xTVpDMllQQkIzbElWV2g2LF9OTGk1WWpYQjBrQnNOUjlUYXNsYjNqcjJIWjBXS2R1LDY2ODMwMjc30200LTh4PI6G/pdf?s=ap', 
        'last_finalization_error': None, 
        'latest_revision': None, 
        'lines': {
            'object': 'list', 
            'data': [
                {
                    'id': 'il_1Mb0fQPBB3lIVWh6bBIsPtlg', 
                    'object': 'line_item', 
                    'amount': 0, 
                    'amount_excluding_tax': 0, 
                    'currency': 'gbp', 
                    'description': 'Trial period for Tots netball - Wednesday - Ely', 
                    'discount_amounts': [
                        {
                            'amount': 0, 
                            'discount': 'di_1Mb0fQPBB3lIVWh65IiMhkkb'
                        }
                    ], 
                    'discountable': True, 
                    'discounts': [], 
                    'livemode': False, 
                    'metadata': {
                        'internal_id': 'c1cccad5-1a5e-49b4-88e2-6d383f4d066a'
                    }, 
                    'period': {
                        'end': 1678103876, 
                        'start': 1676289476
                    }, 
                    'plan': {
                        'id': 'price_1MayJaPBB3lIVWh6fLXNwxW2', 
                        'object': 'plan', 
                        'active': True, 
                        'aggregate_usage': None, 
                        'amount': 2500, 
                        'amount_decimal': '2500', 
                        'billing_scheme': 'per_unit', 
                        'created': 1676280434, 
                        'currency': 'gbp', 
                        'interval': 'month', 
                        'interval_count': 1, 
                        'livemode': False, 
                        'metadata': {
                            'internal_id': 'd57ddd36-706a-4c0a-9cd2-3bd430c6cddb'
                        }, 
                        'nickname': None, 
                        'product': 'prod_NLfe1HGAhBNHqJ', 
                        'tiers_mode': None, 
                        'transform_usage': None, 
                        'trial_period_days': None, 
                        'usage_type': 'licensed'
                    }, 
                    'price': {
                        'id': 'price_1MayJaPBB3lIVWh6fLXNwxW2', 
                        'object': 'price', 
                        'active': True, 
                        'billing_scheme': 'per_unit', 
                        'created': 1676280434, 
                        'currency': 'gbp', 
                        'custom_unit_amount': None, 
                        'livemode': False, 
                        'lookup_key': None, 
                        'metadata': {
                            'internal_id': 'd57ddd36-706a-4c0a-9cd2-3bd430c6cddb'
                        }, 
                        'nickname': None, 
                        'product': 'prod_NLfe1HGAhBNHqJ', 
                        'recurring': {
                            'aggregate_usage': None, 
                            'interval': 'month', 
                            'interval_count': 1, 
                            'trial_period_days': None, 
                            'usage_type': 'licensed'
                        }, 
                        'tax_behavior': 'unspecified', 
                        'tiers_mode': None, 
                        'transform_quantity': None, 
                        'type': 'recurring', 
                        'unit_amount': 2500, 
                        'unit_amount_decimal': '2500'
                    }, 
                    'proration': False, 
                    'proration_details': {
                        'credited_items': None
                    }, 
                    'quantity': 2, 
                    'subscription': 'sub_1Mb0fQPBB3lIVWh6i0W5DIer', 
                    'subscription_item': 'si_NLi5NEkBcift4T', 
                    'tax_amounts': [], 
                    'tax_rates': [], 
                    'type': 'subscription', 
                    'unit_amount_excluding_tax': '0'
                }
            ], 
            'has_more': False, 
            'total_count': 1, 
            'url': '/v1/invoices/in_1Mb0fQPBB3lIVWh6qpHNokN9/lines'
        }, 
        'livemode': False, 
        'metadata': {}, 
        'next_payment_attempt': None, 
        'number': 'B541E386-0011', 
        'on_behalf_of': None, 
        'paid': True, 
        'paid_out_of_band': False, 
        'payment_intent': None, 
        'payment_settings': {
            'default_mandate': None, 
            'payment_method_options': None, 
            'payment_method_types': None
        }, 
        'period_end': 1676289476, 
        'period_start': 1676289476, 
        'post_payment_credit_notes_amount': 0, 
        'pre_payment_credit_notes_amount': 0, 
        'quote': None, 
        'receipt_number': None, 
        'rendering_options': None, 
        'shipping_cost': None, 
        'shipping_details': None, 
        'starting_balance': 0, 
        'statement_descriptor': None, 
        'status': 'paid', 
        'status_transitions': {
            'finalized_at': 1676289476, 
            'marked_uncollectible_at': None, 
            'paid_at': 1676289476, 
            'voided_at': None
        }, 
        'subscription': 'sub_1Mb0fQPBB3lIVWh6i0W5DIer', 
        'subtotal': 0, 
        'subtotal_excluding_tax': 0, 
        'tax': None, 
        'test_clock': None, 
        'total': 0, 
        'total_discount_amounts': [
            {
                'amount': 0, 
                'discount': 'di_1Mb0fQPBB3lIVWh65IiMhkkb'
            }
        ], 
        'total_excluding_tax': 0, 
        'total_tax_amounts': [], 
        'transfer_data': None, 
        'webhooks_delivered_at': None
    }
    
    """
    def __init__(self, data, method):
        self.method = method
        self.data = data
        self.external_id = self.data["id"]
        

    def get(self):
        inv, created = Invoice.objects.get_or_create(external_id=self.external_id)
        return inv

    def deleted(self):
        obj = self.get()
        print_webhook_event(obj, 'deleted')
        obj.status = 0
        obj.save()
        

    def updated(self):
        obj = self.get()
        print_webhook_event(obj, 'updated')

        customer = Customer.objects.get(external_id = self.data["customer"])
        obj.customer = customer
        obj.account = customer.account
        
        if self.data["subscription"]:
            subscription, created = Subscription.objects.get_or_create(external_id = self.data["subscription"])
            subscription.account = obj.account
            subscription.customer = customer
            subscription.save()
            obj.subscription = subscription
            StripeSubscription(subscription).get()
        
        if self.data["default_source"]:
            source = Source.objects.filter(external_id = self.data["default_source"])
            if source.exists():
                obj.source = source.first()
        
        obj.charge = self.data["charge"]

        obj.amount_due = self.data["amount_due"]
        obj.amount_paid = self.data["amount_paid"]
        obj.amount_remaining = self.data["amount_remaining"]
        obj.amount_shipping = self.data["amount_shipping"]
        obj.application_fee_amount = self.data["application_fee_amount"]
        obj.attempt_count = self.data["attempt_count"]
        obj.attempted = self.data["attempted"]
        obj.currency = self.data["currency"]
        obj.invoice_status = self.data["status"]
        obj.subtotal = self.data["subtotal"]
        obj.subtotal_excluding_tax = self.data["subtotal_excluding_tax"]
        obj.tax = self.data["tax"]
        obj.total = self.data["total"]
        obj.total_excluding_tax = self.data["total_excluding_tax"]
        obj.period_end = convert_naive_to_aware(self.data["period_end"])
        obj.period_start = convert_naive_to_aware(self.data["period_start"])

        obj.hosted_invoice_url = self.data["hosted_invoice_url"]
        obj.invoice_pdf = self.data["invoice_pdf"]


        for item in self.data["lines"]["data"]:
            price = Price.objects.get(external_id=item["price"]["id"])
            invoice_item, created = InvoiceItem.objects.get_or_create(external_id = item["id"])
            invoice_item.customer = customer
            invoice_item.account=customer.account
            invoice_item.price=price
            invoice_item.amount=item["amount"]
            invoice_item.quantity=item["quantity"]
            invoice_item.amount_excluding_tax = item["amount_excluding_tax"]
            invoice_item.currency =item["currency"]
            invoice_item.description =item["description"]
            invoice_item.period_end = convert_naive_to_aware(item["period"]["end"])
            invoice_item.period_start =convert_naive_to_aware(item["period"]["start"])
            invoice_item.unit_amount_excluding_tax = item["unit_amount_excluding_tax"]
            invoice_item.save()
            
            obj.invoice_items.add(invoice_item)
        obj.save()
        

    def created(self):
        obj = self.get()
        print_webhook_event(obj, 'created')

        customer = Customer.objects.get(external_id = self.data["customer"])
        obj.customer = customer
        obj.account = customer.account
        
        if self.data["subscription"]:
            subscription, created = Subscription.objects.get_or_create(external_id = self.data["subscription"])
            subscription.account = obj.account
            subscription.customer = customer
            subscription.save()
            obj.subscription = subscription
            StripeSubscription(subscription).get()

        
        if self.data["default_source"]:
            source = Source.objects.filter(external_id = self.data["default_source"])
            if source.exists():
                obj.source = source.first()

        obj.charge = self.data["charge"]

        obj.amount_due = self.data["amount_due"]
        obj.amount_paid = self.data["amount_paid"]
        obj.amount_remaining = self.data["amount_remaining"]
        obj.amount_shipping = self.data["amount_shipping"]
        obj.application_fee_amount = self.data["application_fee_amount"]
        obj.attempt_count = self.data["attempt_count"]
        obj.attempted = self.data["attempted"]
        obj.currency = self.data["currency"]
        obj.invoice_status = self.data["status"]
        obj.subtotal = self.data["subtotal"]
        obj.subtotal_excluding_tax = self.data["subtotal_excluding_tax"]
        obj.tax = self.data["tax"]
        obj.total = self.data["total"]
        obj.total_excluding_tax = self.data["total_excluding_tax"]
        obj.period_end = convert_naive_to_aware(self.data["period_end"])
        obj.period_start = convert_naive_to_aware(self.data["period_start"])
        obj.hosted_invoice_url = self.data["hosted_invoice_url"]
        obj.invoice_pdf = self.data["invoice_pdf"]


        for item in self.data["lines"]["data"]:
            price = Price.objects.get(external_id=item["price"]["id"])
            invoice_item, created = InvoiceItem.objects.get_or_create(external_id = item["id"])
            invoice_item.customer = customer
            invoice_item.account=customer.account
            invoice_item.price=price
            invoice_item.amount=item["amount"]
            invoice_item.quantity=item["quantity"]
            invoice_item.amount_excluding_tax = item["amount_excluding_tax"]
            invoice_item.currency =item["currency"]
            invoice_item.description =item["description"]
            invoice_item.period_end = convert_naive_to_aware(item["period"]["end"])
            invoice_item.period_start =convert_naive_to_aware(item["period"]["start"])
            invoice_item.unit_amount_excluding_tax = item["unit_amount_excluding_tax"]
            invoice_item.save()
            
            obj.invoice_items.add(invoice_item)

        obj.save()
        


