from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from .models import User
from django.conf import settings
from django.core.mail import send_mail


class TokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: User):
        token = super().get_token(user)

        token["email"] = user.email
        token["username"] = user.username
        token["is_active"] = user.is_active
        token["email_verified"] = user.email_verified

        return token


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User

        fields = ("email", "password", "username")

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data["email"],
            username=validated_data["username"],
        )
        user.set_password(validated_data["password"])
        user.save()

        send_mail(
            "indietour email verification",
            f"""Please verify your indietour account.
            Your email verification code is: {user.verification_code}
            """,
            settings.EMAIL_HOST,
            [user.email],
            fail_silently=False,
        )

        return TokenObtainPairSerializer().get_token(user)
