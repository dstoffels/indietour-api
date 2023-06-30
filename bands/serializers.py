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
    user = UserSerializer(read_only=True)

    class Meta:
        model = BandUser
        fields = "user", "id", "is_admin"

    def create(self, validated_data: dict):
        email = self.initial_data.get("email")
        is_admin = self.initial_data.get("is_admin")
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
import json


class BandSerializer(BaseSerializer):
    class Meta:
        model = Band
        fields = "id", "name", "is_archived", "owner", "users", "tours"

    owner = UserSerializer(read_only=True)
    users = BandUserSerializer(source="banduser_set", many=True, read_only=True)
    tours = TourSerializer(source="tour_set", many=True, read_only=True)

    def create(self, validated_data):
        validated_data["owner"] = self.user
        return super().create(validated_data)

    def to_representation(self, instance: Band):
        many = self.context.get("many")
        archived_bands = self.context.get("archived_bands")
        include = self.context.get("include")

        if many and not archived_bands and instance.is_archived:
            return None

        band_dict = super().to_representation(instance)

        if include is None:
            band_dict.pop("tours")
            return band_dict

        if include in ["dates", "all"]:

            def tour_sorter(tour):
                first_date = tour.get("dates")[0].get("date") if len(tour.get("date")) else ""
                return first_date

            tours = band_dict.get("tours")
            band_dict["tours"] = sorted(tours, key=tour_sorter)

        return band_dict
