from rest_framework import serializers
from .models import Tour, TourUser
from authentication.serializers import UserSerializer
from authentication.models import User
from rest_framework.exceptions import ValidationError
from authentication.utils import generate_password
from django.core.mail import send_mail
from django.conf import settings
from bands.serializers import BandUserSerializer
from django.shortcuts import get_object_or_404


class TourUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourUser
        fields = "id", "banduser", "tour_id"

    banduser = BandUserSerializer(read_only=True)

    def create(self, validated_data):
        from bands.serializers import BandUserSerializer, BandUser, Band

        email = self.initial_data.get("email")
        tour_id = validated_data.get("tour_id")
        band_id = self.initial_data.get("band_id")
        band = get_object_or_404(Band, id=band_id)
        tour: Tour = get_object_or_404(Tour, id=tour_id)

        try:
            banduser = BandUser.objects.get(user__email=email)
        except:
            ser = BandUserSerializer(data=self.initial_data, context={"band": band})
            ser.is_valid(raise_exception=True)
            ser.save()
            banduser = ser.instance

        touruser = TourUser.objects.filter(tour=tour, banduser=banduser).first()
        if not touruser:
            touruser = TourUser.objects.create(tour=tour, banduser=banduser)
        return touruser


from dates.serializers import DateSerializer


class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = ("id", "name", "is_archived", "band_id", "users", "dates")

    users = TourUserSerializer(source="touruser_set", read_only=True, many=True)
    dates = DateSerializer(read_only=True, many=True)

    def create(self, validated_data: dict):
        duplicate = Tour.objects.filter(band_id=validated_data.get("band_id"), name=validated_data.get("name")).first()
        if duplicate:
            raise ValidationError({"details": "Cannot have duplicate tours.", "code": "DUPLICATE"})
        return super().create(validated_data)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        dates = rep["dates"]
        rep["dates"] = sorted(dates, key=lambda d: d["date"])
        return rep
