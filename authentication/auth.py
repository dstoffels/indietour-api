from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.request import Request


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        raw_access_token = request.COOKIES.get("access")
        if raw_access_token is None:
            return None

        validated_token: AccessToken = self.get_validated_token(raw_access_token)

        return self.get_user(validated_token), validated_token
