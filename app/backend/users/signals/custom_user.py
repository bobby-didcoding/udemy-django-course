# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django.db.models.signals import pre_save
from django.contrib.auth import get_user_model

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.conf import settings
from django.http import JsonResponse
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import get_connection

# --------------------------------------------------------------
# Project imports
# --------------------------------------------------------------
from ecommerce.models import Customer, Cart
from utils.decorators import suspendingreceiver


User = get_user_model()

@suspendingreceiver(pre_save, sender=User, weak=False)
def create_ecommerce_objects(sender, instance, **kwargs):
    try:
        current = instance
        previous = sender.objects.get(id = instance.id)
        if previous.is_active == False and current.is_active:
            customer = Customer.objects.create(user = instance)
            Cart.objects.create(customer = customer)

            site_id = settings.SITE_ID
            current_site = Site.objects.get(id = site_id).domain
            if settings.PRODUCTION:
                protocol = "https://"
            else:
                protocol = "http://"
            context = {
                    'invoice_url': instance.hosted_invoice_url,
                    'domain':f'{protocol}{current_site}',
                    'support_email':settings.EMAIL_HOST_USER
                }

            html_content = render_to_string('users/emails/welcome-email.html', context ) # render with dynamic value
            text_content = strip_tags(html_content) # Strip the html tag. So people can see the pure text at least.
        
            with get_connection(
                    host= settings.EMAIL_HOST,
                    port= settings.EMAIL_PORT,
                    username=settings.EMAIL_HOST_USER,
                    password=settings.EMAIL_HOST_PASSWORD,
                    use_tls=settings.EMAIL_USE_TLS,
                ) as connection:
                    msg = EmailMultiAlternatives(
                        'Welcome',
                        text_content,
                        f'{settings.DISPLAY_NAME} <{settings.EMAIL_HOST_USER}>',
                        [instance.email],
                        cc=[],
                        bcc=[],
                        connection=connection)
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
    except sender.DoesNotExist:
        pass