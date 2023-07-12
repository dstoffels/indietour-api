import secrets
import string
from rest_framework.response import Response
from django.conf import settings
from datetime import datetime

# from .serializers import User, UserSerializer


def generate_verification_code():
    chars = string.digits
    return "".join(secrets.choice(chars) for _ in range(6))


def generate_password():
    chars = [*string.ascii_letters, *string.digits]
    return "".join(secrets.choice(chars) for _ in range(12))


def generate_user_response(token_pair, user):
    from .serializers import UserSerializer

    response = Response(data=UserSerializer(user).data, status=200)

    access = token_pair.get("access")
    access_expiry = datetime.utcnow() + settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]
    response.set_cookie("access", access, expires=access_expiry, httponly=True, secure=True, samesite="Strict")

    refresh = token_pair.get("refresh")
    refresh_expiry = datetime.utcnow() + settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"]
    response.set_cookie("refresh", refresh, expires=refresh_expiry, httponly=True, secure=True, samesite="Strict")

    return response
