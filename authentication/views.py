from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.request import Request
from .serializers import RegistrationSerializer, UserSerializer, LoginSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from .models import User
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from .utils import generate_verification_code
from django.utils import timezone
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime
from django.conf import settings


class AuthCookieBaseView(generics.GenericAPIView):
    def get_token_pair(self, user: User):
        refresh: RefreshToken = RefreshToken.for_user(user)
        return {"access": str(refresh.access_token), "refresh": str(refresh)}

    def get_response(self, user, token_pair, status=200):
        response = Response(data=UserSerializer(user).data, status=status)
        self.set_cookies(response, token_pair)
        return response

    def set_cookies(self, response: Response, token_pair: dict):
        access = token_pair.get("access")
        access_expiry = datetime.utcnow() + settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]
        response.set_cookie(
            "access",
            access,
            expires=access_expiry,
            httponly=True,
            secure=True,
            samesite="None",
        )

        refresh = token_pair.get("refresh")
        refresh_expiry = (
            datetime.utcnow() + settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"]
        )
        response.set_cookie(
            "refresh",
            refresh,
            expires=refresh_expiry,
            httponly=True,
            secure=True,
            samesite="None",
        )


class LoginView(TokenObtainPairView, AuthCookieBaseView):
    permission_classes = (AllowAny,)

    def post(self, request: Request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = User.objects.get(email=request.data.get("email"))
        token_pair = response.data
        return self.get_response(user, token_pair)


class LogoutView(AuthCookieBaseView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        response = Response(data=None)
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        return response


class RefreshView(TokenRefreshView, AuthCookieBaseView):
    permission_classes = (AllowAny,)

    def post(self, request: Request, *args, **kwargs):
        refresh = request.COOKIES.get("refresh")
        if not refresh:
            return Response(None)
            # raise ValidationError({"detail": "No refresh token provided"}, 401)

        request.data["refresh"] = refresh

        token_pair = super().post(request, *args, **kwargs).data

        jwt_auth = JWTAuthentication()
        access = token_pair.get("access")
        valid_token = jwt_auth.get_validated_token(access)
        user = jwt_auth.get_user(valid_token)

        return self.get_response(user, token_pair)


class RegisterView(generics.CreateAPIView, AuthCookieBaseView):
    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        # create new user
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        self.perform_create(ser)

        # login new user
        user = User.login(request)
        token_pair = self.get_token_pair(user)
        return self.get_response(user, token_pair, status=201)


class UserView(generics.RetrieveUpdateAPIView, AuthCookieBaseView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request, *args, **kwargs):
        return Response(UserSerializer(request.user).data, 200)

    def patch(self, request: Request, *args, **kwargs):
        user: User = request.user
        ser = UserSerializer(user, data=request.data, partial=True)
        ser.is_valid()
        ser.save()

        token_pair = self.get_token_pair(user)
        return self.get_response(user, token_pair)


class UserVerifyView(generics.CreateAPIView, AuthCookieBaseView):
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

To verify, log in to your account at indietour.org and you will be directed to enter your verification code.
""",
            settings.EMAIL_HOST,
            [user.email],
            fail_silently=False,
        )
        return Response(
            {
                "detail": f"An email with a new verification code has been sent to {user.email}. "
            },
            status=200,
        )

    def post(self, request: Request, *args, **kwargs):
        verification_code = request.data.get("verification_code")
        user: User = request.user
        if user.verification_code == verification_code:
            user.email_verified = True
            user.save()
            token_pair = self.get_token_pair(user)
            return self.get_response(user, token_pair)
        raise ValidationError(
            {"detail": "Invalid verification code", "code": "BAD_CREDENTIALS"}
        )


class UserPasswordView(generics.CreateAPIView, AuthCookieBaseView):
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request, *args, **kwargs):
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        user: User = request.user

        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            token_pair = self.get_token_pair(user)
            return self.get_response(user, token_pair)

        raise ValidationError(
            {"detail": "Invalid credentials", "code": "BAD_CREDENTIALS"}
        )
