from django.shortcuts import render
from rest_framework import generics
from rest_framework_simplejwt.tokens import Token
from .serializers import RegistrationSerializer, TokenSerializer, UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from django.shortcuts import get_object_or_404


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
        return Response(
            {"refresh": str(token), "access": str(token.access_token)},
            201,
        )


class UserView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def patch(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=request.user.id)
        ser = UserSerializer(user, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        token = TokenSerializer().get_token(user)
        return Response(
            {"refresh": str(token), "access": str(token.access_token)},
            200,
        )
