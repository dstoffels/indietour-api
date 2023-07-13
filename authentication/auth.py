from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        raw_access_token = request.COOKIES.get("access")

        if raw_access_token:
            validated_token = self.get_validated_token(raw_access_token)

            return self.get_user(validated_token), validated_token
