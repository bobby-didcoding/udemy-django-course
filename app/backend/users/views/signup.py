# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django.shortcuts import render, redirect, reverse
from django.views import generic
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate,update_session_auth_hash
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings
from django.http import JsonResponse


# --------------------------------------------------------------
# App imports
# --------------------------------------------------------------
from .models import UserToken
from .forms import (UserForm,ForgottenPasswordForm,	AuthForm,
	RequestPasswordForm,UserBioForm,UserAvatarForm,	ChangePasswordForm,
    UserAlterationForm, UserProfileForm)



# --------------------------------------------------------------
# Project imports
# --------------------------------------------------------------
from utils.decorators import login_forbidden
from tasks.tasks import create_email
from utils.mixins import (AjaxFormMixin, reCAPTCHAValidation,FormErrors,
	RedirectParams,	TokenGenerator, get_avatar
	)
from projects.models import Project


class SignUpView(AjaxFormMixin, generic.FormView):
    '''
    Basic view for user sign up with reCAPTURE security
    '''
    template_name = "users/sign_up.html"
    form_class = UserForm
    success_url = '/members/account/'

    #over write the mixin logic to get, check and save reCAPTURE score
    #send a verification email via Celery
    def form_valid(self, form):
        response = super(AjaxFormMixin, self).form_valid(form)
        data = {"result": "Error","message": "Something went wrong","redirect": False}
        if self.request.is_ajax():
            #failsafe! check & make sure the user has ticked the T&C's checkbox
            terms = form.cleaned_data.get('terms')
            match terms:
                case "false":
                    data["message"] = "You must agree to our terms and conditions to sign up"
                case _:
                    news =  form.cleaned_data.get('news')
                    token = form.cleaned_data.get('token')
                    #validate sign up with reCapture
                    captcha = reCAPTCHAValidation(token)
                    match captcha["success"]:
                        case True:
                            user = form.save()
                            user.email = user.username
                            user.save()
                            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')

                            #write a function to handle news letter checkbox

                            #create a new token
                            token = TokenGenerator()
                            make_token = token.make_token(user)
                            url_safe = urlsafe_base64_encode(force_bytes(user.pk))

                            #Create a usertoken object to store token
                            ut = UserToken.objects.create(
                                user=user,
                                token = make_token,
                                is_email = True)

                            #this is a celery task
                            #send verification email
                            create_email.delay(
                                user_id = user.id, #user ID - this must be added
                                internal=False,
                                email_account = "donotreply",#the email account being used
                                subject = 'Verify your email',
                                email = user.email,#who to email
                                cc = [],
                                template = "email/users/verification_email.html",#template to be used
                                context = {
                                    'token': make_token,
                                    'url_safe': url_safe
                                }
                                )

                            #this is a celery task
                            #send email to main internal email
                            create_email.delay(
                                user_id = None, #user ID - this must be added
                                internal=True,
                                email_account = "donotreply",#the email account being used
                                subject = 'A user has signed up',
                                email = settings.EMAIL_HOST_USER,#who to email
                                cc = [],
                                template = "email/users/new_user.html",#template to be used
                                context = {'admin_link': f'admin/auth/user/{user.id}/change/'}
                            )

                            

                            data['result'] = 'Success'
                            data['message']="Thank you for signing up"
                            data['redirect']= "/members/account/"
                            return JsonResponse(data)
                        case _:
                            data['message']="We can not validate your submission"
            return JsonResponse(data)
        return response

    @method_decorator(login_forbidden)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

