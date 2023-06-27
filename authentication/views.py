from rest_framework import generics
from rest_framework.request import Request
from .serializers import RegistrationSerializer, TokenSerializer, UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from .models import User
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from .utils import generate_verification_code


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
""",
            settings.EMAIL_HOST,
            [user.email],
            fail_silently=False,
        )
        return Response("", 200)

    def post(self, request: Request, *args, **kwargs):
        verification_code = request.data.get("verification_code")
        user: User = request.user
        if user.verification_code == verification_code:
            user.email_verified = True
            user.save()
            token = TokenSerializer().get_token(user)
            return Response(
                {"refresh": str(token), "access": str(token.access_token)},
                200,
            )
        else:
            return Response({"detail": "Invalid verification code"}, 400)
