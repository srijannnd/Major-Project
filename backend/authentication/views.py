from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from authentication.serializers import *
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .renderers import UserJSONRenderer
import jwt, requests
from django.conf import settings

# Create your views here.


class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    # renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data
        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data
        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't  have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserFlag(APIView):

    def post(self, request):
        token = request.data
        flag = 0
        user_id = 0
        if 'token' in token:
            try:
                user = jwt.decode(token['token'], settings.SECRET_KEY, algorithms=['HS256'])
                if User.objects.filter(id=user['id']).exists():
                    flag = 1
                    user_id = user['id']
            except Exception:
                pass
        return Response({'flag': flag, 'id': user_id}, status=status.HTTP_200_OK)


