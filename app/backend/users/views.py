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


class SignInView(AjaxFormMixin, generic.FormView):
    '''
    View for user sign in
    '''
    template_name = "users/sign_in.html"
    form_class = AuthForm
    success_url = '/members/account/'

    def form_valid(self, form):
        response = super(AjaxFormMixin, self).form_valid(form)
        if self.request.is_ajax():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            #attempt to authenticate user
            user = authenticate(self.request, username=username, password=password)
            if user is not None:
                login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
                data = {
                    "result": "Success",
                    "message": 'You are now logged in',
                    "redirect": self.request.POST.get("next", "/members/account/")
                    }
                return JsonResponse(data)
            else:
                data = {
                    "result": "Error",
                    "message": FormErrors(form),
                    "redirect": False
                    }
                return JsonResponse(data)
        return response

    @method_decorator(login_forbidden)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



def sign_out(request):
	'''
	Basic view for user sign out
	'''
	logout(request)
	return redirect(reverse('core:home'))




class ForgottenPasswordView(AjaxFormMixin, generic.FormView):
    '''
    View for users to request a new password
    '''
    template_name = "users/forgotten_password.html"
    form_class = RequestPasswordForm
    success_url = "/"

    def form_valid(self, form):
        response = super(AjaxFormMixin, self).form_valid(form)
        if self.request.is_ajax():
            username = form.cleaned_data.get('email')
            #check if user exists
            try:
                user = User.objects.get(username = username)
            except User.DoesNotExist:
                message = "Email address is not saved in our system. Perhaps you signed up using a social account?"
                return JsonResponse({"result": "ERROR", "message": message, "redirect": False})

            #create a new token
            token = TokenGenerator()
            make_token = token.make_token(user)
            url_safe = urlsafe_base64_encode(force_bytes(user.pk))

            ut = UserToken.objects.create(
                user=user,
                token = make_token,
                is_password = True)

            #this is a celery task
            #send password reset
            create_email.delay(
                user_id = user.id, #user ID - this must be added
                email_account = "donotreply",#the email account being used
                subject = 'Password reset',
                email = user.email,#who to email
                cc = [],
                template = "email/users/password_email.html",#template to be used
                context = {
                    'token': make_token,
                    'url_safe': url_safe
                }
                )
            data = {
                "result": "Success",
                "message": 'You will receive an email to reset your password',
                "redirect": "/"
                }
            return JsonResponse(data)
        else:
            data = {
                "result": "Error",
                "message": FormErrors(form),
                "redirect": False
                }
            return JsonResponse(data)
        return response

    @method_decorator(login_forbidden)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@login_required
def email(request):
    '''
    AJAX function to request email view for registered users
    '''
    if request.method == "POST":

        user = request.user
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
            email_account = "donotreply",#the email account being used
            subject = 'Verify your email',
            email = user.email,#who to email
            cc = [],
            template = "verification_email.html",#template to be used
            context = {
                'token': make_token,
                'url_safe': url_safe
            }
            )

        data = {
            "result": "Success",
            "message": 'We have sent you an email to verify',
            "redirect": '/members/account/'
            }
        return JsonResponse(data)


def verification(request, uidb64, token):
    '''
    Function view to handle verification tokens
    '''
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        ut = UserToken.objects.active().get(user = user, token = token)
        email_token = ut.is_email
        password_token = ut.is_password

    except(TypeError, ValueError, OverflowError, User.DoesNotExist, UserToken.DoesNotExist):

        #user our RedirectParams function to redirect & append 'token_error' parameter to fire an error message
        return RedirectParams(url = 'users:sign-in', params = {"token_error": "true"})

    #if User & UserToken exist...
    if user and ut:

        # if the token type is_email
        if email_token:

            #deactivate the token now that it has been used
            ut.status = 0
            ut.save()

            up = user.userprofile
            up.email_verified = True
            up.save()

            #login the user
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            #user our RedirectParams function to redirect & append 'verified' parameter to fire a success message
            return RedirectParams(url = 'users:account', params = {"verified": "true"})

        # if the token is a password token
        elif password_token:

            fp_form = ForgottenPasswordForm(user = user)

            if request.is_ajax() and request.method == "POST":
                fp_form = ForgottenPasswordForm(data = request.POST, user = user)
                if fp_form.is_valid():

                    fp_form.save()
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')

                    #deactivate the token now that it has been used
                    ut.status = 0
                    ut.save()
                    data = {
                        "result": "Success",
                        "message": 'Your password has been updated',
                        "redirect": '/members/account/'
                        }
                    return JsonResponse(data)

                else:
                    data = {
                        "result": "Error",
                        "message": FormErrors(fp_form),
                        "redirect": False
                        }
                    return JsonResponse(data)

            context = {'fp_form':fp_form, "uidb64":uidb64, "token":token}
            return render(request, 'users/verification.html', context)



class AccountView(generic.ListView):
    '''
    basic stats view
    '''
    template_name = "users/account.html"
    paginate_by = 50
    model = Project

    def get_queryset(self):
        qs = Project.objects.active().filter(author = self.request.user)
        return qs

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



@login_required
def ProfileView(request):
    '''
    View for users to request a new password
    '''
    user = request.user
    up = user.userprofile

    bio_form = UserBioForm(instance = up)
    avatar_form = UserAvatarForm(instance = up)
    user_form = UserAlterationForm(instance = user)
    password_form = ChangePasswordForm(user = user)
    user_profile_form = UserProfileForm(instance = up)


    form_holder = {
        'user_bio_form': UserBioForm,
        'user_avatar_form':UserAvatarForm,
        'user_alteration_form': UserAlterationForm,
        'user_password_form': ChangePasswordForm,
        'user_profile_form': UserProfileForm
    }

    if request.method == "POST":
        data = {"result": "Error","message": "Something went wrong","redirect": False}
        for key in form_holder.keys():
            form_label = request.POST.get("form_label")
            # If the key is the same as the formlabel, we should use the posted data
            if form_label == key:

                # Get the form and initiate it with the sent data
                img = request.FILES.get("FILE",None)

                print(img)
                match key:
                    case "user_alteration_form":
                        form = form_holder.get(key)(data = request.POST, instance = user)
                    case "user_password_form":
                        form = form_holder.get(key)(data = request.POST, user = user)
                    case "user_bio_form"|"user_profile_form":
                        form = form_holder.get(key)(data = request.POST, instance = up)
                    case "user_avatar_form":
                        form = form_holder.get(key)(data = request.POST, files = request.FILES, instance = up)
                if form.is_valid():
                    form.save()
                    #update the session with the new password
                    if key == "user_password_form":
                        update_session_auth_hash(request, form.user)

                    if key == "user_alteration_form":
                        up.has_profile = True
                        up.save()

                    # if form_label == "user_alteration_form":

                    #     avatar = get_avatar(user)
                    #     up.avatar.save(avatar["file_name"], avatar["file"])

                    data = {
                    "result": "Success",
                    "message": 'Your profile has been updated',
                    "redirect": '/members/account/'
                    }
                    if img:
                        data["avatar"] = up.avatar.url
                    if key == 'user':
                        data['user'] = f'{user.first_name} {user.last_name}'
                    return JsonResponse(data)
                else:
                    data = {
                    "result": "Error",
                    "message": FormErrors(form),
                    "redirect": False
                    }
                    return JsonResponse(data)

    else:
        #this is the get request
        context = {
            'bio_form': bio_form,
            'avatar_form': avatar_form,
            'user_form': user_form,
            'password_form': password_form,
            'up_form': user_profile_form
        }

        #passes 'verified' parameter to url to handle a success message
        verified = request.GET.get("verified",None)
        if verified:
            messages.success(request, 'Thank you for verifying your email address')

        email_msg = request.GET.get("email", "true")
        context["email_msg"] = email_msg


        return render(request, 'users/profile.html', context)





# --------------------------------- API's -------------------------------





def UserProfileAPI(request):
	'''
	API function to serialize UserProfile objects
	'''

	result = "Error"
	message = "Something went wrong"
	data = {}
	if request.method == "POST":

		query_dict = {}
		if query_dict:
			serializer = json.dumps(UserProfileSerializer(UserProfile.objects.filter(**query_dict), many=True).data)
		else:
			serializer = json.dumps(UserProfileSerializer(UserProfile.objects.all(), many=True).data)
		data = json.loads(serializer)
		result = "Success"
		message = "Here are you requested UserProfile objects"
		return JsonResponse({'result': result, 'message': message, 'data': data})
	return JsonResponse({'result': result, 'message': message, 'data': data})
