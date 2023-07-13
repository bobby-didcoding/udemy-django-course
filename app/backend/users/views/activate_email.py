# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings as django_settings
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

# --------------------------------------------------------------
# Project Party imports
# --------------------------------------------------------------
from utils.mixins import AccountActivationTokenGenerator

# --------------------------------------------------------------
# 3rd Party imports
# --------------------------------------------------------------
from djoser import email
from djoser.conf import settings

User = get_user_model()
account_activation_token = AccountActivationTokenGenerator()


class ActivationEmail(email.ActivationEmail):
    template_name = 'emails/users/activate_email.html'

    def get_context_data(self):
        context = super().get_context_data()
        user = context.get("user")
        context['user'] = user.get_full_name()
        context["uid"] = urlsafe_base64_encode(force_bytes(user.pk))
        context["token"] = account_activation_token.make_token(user)
        context["url"] = settings.ACTIVATION_URL.format(**context)
        return context
    
    def send(self, to, *args, **kwargs):
        self.to = to
        context = self.get_context_data()
        subject = f"Activate your account"
        message = render_to_string(self.template_name, {
                'user': context.get("user"),
                'protocol':context.get('protocol'),
                'domain': context.get('domain'),
                'uid': context.get('uid'),
                'token': context.get('token'),
                'url': context.get('url'),
        })
        send_mail(subject, message=subject,recipient_list=self.to, from_email=None, html_message=message, fail_silently=False)
