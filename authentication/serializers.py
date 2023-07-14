from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from .models import User
from django.conf import settings
from django.core.mail import send_mail


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def is_valid(self, *, raise_exception=True):
        return super().is_valid(raise_exception=raise_exception)


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ("email", "password", "username")

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data["password"])
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
        return user


class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    email_verified = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ("email", "username", "is_active", "email_verified")
