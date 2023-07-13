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
from users.serializers import CustomUserSerializer

# --------------------------------------------------------------
# 3rd Party imports
# --------------------------------------------------------------
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import parsers
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class CustomUserViewSet(APIView):
    """
    A simple ViewSet for retrieving and updating custom users.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomUserSerializer

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        try:
            data = parsers.JSONParser().parse(request)
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                return JsonResponse(serializer.data, status=200)
            return JsonResponse(serializer.errors, status=400)
        except JSONDecodeError:
            return JsonResponse({"result": "error","message": "Json decoding error"}, status= 400)
