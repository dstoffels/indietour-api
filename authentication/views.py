from rest_framework import generics
from rest_framework.request import Request
from .serializers import RegistrationSerializer, TokenSerializer, UserSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from .models import User
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from .utils import generate_verification_code
from django.contrib.auth import authenticate
from django.utils import timezone


class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request: Request, *args, **kwargs):
        token_pair = super().post(request, *args, **kwargs).data

        user = authenticate(request, email=request.data.get("email"), password=request.data.get("password"))

        if user:
            user.last_login = timezone.now()
            user.save()

        response = Response(data=UserSerializer(user).data, status=200)
        response.set_cookie("jwt-access", token_pair.get("access"), httponly=True, secure=False, samesite="Strict")
        response.set_cookie("jwt-refresh", token_pair.get("refresh"), httponly=True, secure=False, samesite="Strict")

        return response


class RegisterView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        user_ser = self.get_serializer(data=request.data)
        user_ser.is_valid(raise_exception=True)
        self.perform_create(user_ser)

        user = authenticate(request, email=request.data.get("email"), password=request.data.get("password"))

        if user:
            user.last_login = timezone.now()
            user.save()

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


class UserVerifyView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request, *args, **kwargs):
        user: User = request.user
        user.verification_code = generate_verification_code()
        user.save()
        send_mail(
            "Verify your email to begin using indietour",
            f"""Verify your email address so we know it’s really you.
Your email verification code is: {user.verification_code}

To verify, log in to your account at indietour.app/login and you will be directed to enter your verification code.
""",
            settings.EMAIL_HOST,
            [user.email],
            fail_silently=False,
        )
        return Response(
            {"detail": f"An email with a new verification code has been sent to {user.email}. "}, status=200
        )

    def post(self, request: Request, *args, **kwargs):
        verification_code = request.data.get("verification_code")
        user: User = request.user
        if user.verification_code == verification_code:
            user.email_verified = True
            user.save()
            token = TokenSerializer().get_token(user)
            return Response({"refresh": str(token), "access": str(token.access_token)}, 200)
        raise ValidationError({"detail": "Invalid verification code", "code": "BAD_CREDENTIALS"})


class UserPasswordView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request, *args, **kwargs):
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        user: User = request.user

        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            token = TokenSerializer().get_token(user)
            return Response({"refresh": str(token), "access": str(token.access_token)}, 200)

        raise ValidationError({"detail": "Incorrect credentials", "code": "BAD_CREDENTIALS"})
