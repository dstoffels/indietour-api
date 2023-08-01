from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
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
    is_band_admin = serializers.SerializerMethodField()

    def get_is_band_admin(self, user: User):
        from bands.models import Band

        band: Band = Band.objects.filter(id=user.active_band_id).first()
        return bool(band) and band.owner == user or bool(band.bandusers.filter(user=user, is_admin=True).first())

    is_tour_admin = serializers.SerializerMethodField()

    def get_is_tour_admin(self, user: User):
        from tours.models import Tour

        tour: Tour = Tour.objects.filter(id=user.active_tour_id).first()
        return (
            bool(tour)
            and tour.band.owner == user
            or bool(tour.tourusers.filter(banduser__user=user, is_admin=True).first())
        )

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "is_active",
            "email_verified",
            "active_band_id",
            "active_tour_id",
            "is_band_admin",
            "is_tour_admin",
        )
