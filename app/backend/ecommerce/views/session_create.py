# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------

from django.shortcuts import  render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


# --------------------------------------------------------------
# App imports
# --------------------------------------------------------------
from ecommerce.models import Session

# --------------------------------------------------------------
# project imports
# --------------------------------------------------------------
from notifications.models import Notification
from utils.abstracts import MustBeParentView
from events.utils import CampBookingHandler, BookingHandler
from utils.fields.enums import ExperienceType
from users.models import Squaddy

@login_required
def session_create(request):
    """
    handles the creation of a Stripe session
    """
    data = {'result': 'Error', 'message': "Something went wrong, please try again", "redirect": False}
    if request.method == "POST" and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        
        cart = request.user.cart_customer # We will need a signal
        checkout_url = '/' # We will wire up the stripe API soon

        data.update({
            "redirect": checkout_url,
            "result": "Success",
            "message": "Ready to pay"
        })
        return JsonResponse(data)
    else:
        return JsonResponse(data)
