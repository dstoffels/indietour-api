from rest_framework import serializers
from .models import Band, BandUser
from authentication.serializers import UserSerializer
from authentication.models import User
from rest_framework.exceptions import ValidationError
from authentication.utils import generate_password
from django.core.mail import send_mail
from django.conf import settings
from core.serializers import BaseSerializer
from django.shortcuts import get_object_or_404


class BandUserSerializer(BaseSerializer):
    class Meta:
        model = BandUser
        fields = "id", "email", "is_admin", "username"

    email = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField(read_only=True)

    def get_email(self, banduser: BandUser):
        return banduser.user.email

    def get_username(self, banduser: BandUser):
        return banduser.user.username

    def create(self, validated_data: dict):
        email = self.initial_data.get("email")
        is_admin = validated_data.get("is_admin")
        band_id = self.context.get("band_id")

        user, created = User.objects.get_or_create(email=email)

        if created:
            band = get_object_or_404(Band, id=band_id)

            password = generate_password()
            user.set_password(password)
            user.save()
            send_mail(
                f"You have been added to {band.name} on indietour",
                f"""Your indietour account has been created and you've been added to {band.name}!
                
Verify your email address so we know it’s really you.
Your email verification code is: {user.verification_code}

You have been assigned a temporary password and recommend you update it upon first login.
Your temporary password is: {password}.

To verify, log in to your account at indietour.app/login and you will be directed to enter your verification code.
""",
                settings.EMAIL_HOST,
                [email],
                fail_silently=False,
            )

        banduser = BandUser.objects.filter(band_id=band_id, user=user).first()
        if banduser:
            return banduser
        banduser = BandUser.objects.create(band_id=band_id, user=user, is_admin=is_admin)

        return banduser


# BAND SERIALIZER
from tours.serializers import TourSerializer


class BandSerializer(BaseSerializer):
    class Meta:
        model = Band
        fields = "id", "name", "is_archived", "owner", "band_users", "tours"

    owner = UserSerializer(read_only=True)
    band_users = BandUserSerializer(source="bandusers", many=True, read_only=True)
    tours = serializers.SerializerMethodField()

    def get_tours(self, band: Band):
        tours = band.tours.all().order_by("name")
        if not self.archived_tours:
            tours = tours.filter(is_archived=False)
        return TourSerializer(tours, many=True, context=self.context).data

    def create(self, validated_data):
        validated_data["owner"] = self.user
        return super().create(validated_data)

    def get_fields(self):
        fields = super().get_fields()
        if self.include not in ["tours", "dates", "all"]:
            fields.pop("tours")
        return fields

    def init_query_params(self):
        self.archived_tours = False
        self.include = ""


class BandsSerializer(BandSerializer):
    many = True

    def get_fields(self):
        fields = super().get_fields()
        return fields

    def init_query_params(self):
        super().init_query_params()
        self.archived_bands = False
