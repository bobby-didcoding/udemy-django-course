# --------------------------------------------------------------
# Python imports
# --------------------------------------------------------------
from json import JSONDecodeError

# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django.http import JsonResponse


# --------------------------------------------------------------
# App imports
# --------------------------------------------------------------
from users.serializers import AccountSerializer

# --------------------------------------------------------------
# 3rd Party imports
# --------------------------------------------------------------
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import parsers
from rest_framework.views import APIView


class CustomUserViewSet(APIView):

    serializer_class = AccountSerializer

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        
        try:
            data = parsers.JSONParser().parse(request)
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        except JSONDecodeError:
            return JsonResponse({"result": "error","message": "Json decoding error"}, status= 400)

