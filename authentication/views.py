from django.shortcuts import render
from rest_framework import generics
from rest_framework_simplejwt.tokens import Token
from .serializers import RegistrationSerializer, TokenSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status


class LoginView(TokenObtainPairView):
    serializer_class = TokenSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        user_ser = self.get_serializer(data=request.data)
        user_ser.is_valid(raise_exception=True)
        self.perform_create(user_ser)
        token = TokenSerializer().get_token(user_ser.instance)
        return Response({"access": str(token.access_token), "refresh": str(token)}, 201)
