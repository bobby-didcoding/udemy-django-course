# --------------------------------------------------------------
# Python imports
# --------------------------------------------------------------
from json import JSONDecodeError

# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django.http import JsonResponse
from django.contrib.auth import get_user_model


# --------------------------------------------------------------
# App imports
# --------------------------------------------------------------
from users.serializers import RegisterSerializer
from users.models import Referral

# --------------------------------------------------------------
# 3rd Party imports
# --------------------------------------------------------------
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import parsers
from rest_framework.views import APIView

User = get_user_model()

class RegisterAndObtainAuthToken(APIView):

    serializer_class = RegisterSerializer

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)
    
    
    def handle_referral(self, referral_id, user):
        referral_user_obj = User.objects.filter(id = referral_id)
        if referral_user_obj.exists():
            referral_user_obj = referral_user_obj.first()
            referral_obj, created = Referral.objects.get_or_create(user = referral_user_obj)
            referral_obj.signups.add(user)
            referral_obj.save()
    
    
    def post(self, request, *args, **kwargs):
        
        try:
            data = parsers.JSONParser().parse(request)
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)

            #handle referral
            referral_id = request.query_params.get('referral_id')
            if referral_id is not None:
                self.handle_referral(referral_id, user)

            return Response({'token': token.key})
        except JSONDecodeError:
            return JsonResponse({"result": "error","message": "Json decoding error"}, status= 400)

