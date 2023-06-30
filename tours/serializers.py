from .models import Tour, TourUser
from rest_framework.exceptions import ValidationError
from bands.serializers import BandUserSerializer, serializers
from core.serializers import BaseSerializer
from datetime import datetime


class TourUserSerializer(BaseSerializer):
    class Meta:
        model = TourUser
        fields = "id", "banduser"

    banduser = BandUserSerializer(read_only=True)

    def create(self, validated_data):
        from bands.serializers import BandUserSerializer, BandUser

        email = self.initial_data.get("email")
        tour_id = self.context.get("tour_id")

        try:
            banduser = BandUser.objects.get(user__email=email)
        except:
            ser = BandUserSerializer(data=self.initial_data, context=self.context)
            ser.is_valid(raise_exception=True)
            ser.save()
            banduser = ser.instance

        touruser = TourUser.objects.filter(tour_id=tour_id, banduser=banduser).first()
        if not touruser:
            touruser = TourUser.objects.create(tour_id=tour_id, banduser=banduser)
        return touruser


# TOUR SERIALIZER
from dates.serializers import DateSerializer


class TourSerializer(BaseSerializer):
    class Meta:
        model = Tour
        fields = ("id", "name", "is_archived", "band_id", "users", "dates")

    users = TourUserSerializer(source="touruser_set", read_only=True, many=True)
    dates = serializers.SerializerMethodField()

    def get_dates(self, tour: Tour):
        past_dates = self.context.get("past_dates")
        dates = tour.dates.all()
        if not past_dates:
            dates = dates.filter(date__gte=datetime.now().date())
        return DateSerializer(dates, many=True, context=self.context).data

    def create(self, validated_data: dict):
        validated_data["band_id"] = self.context.get("band_id")
        duplicate = Tour.objects.filter(band_id=validated_data.get("band_id"), name=validated_data.get("name")).first()
        if duplicate:
            raise ValidationError({"details": "Cannot have duplicate tours.", "code": "DUPLICATE"})
        return super().create(validated_data)

    def to_representation(self, instance: Tour):
        tour_dict = super().to_representation(instance)
        include = self.context.get("include")

        if include not in ["all", "dates"]:
            tour_dict.pop("dates")
        else:
            dates = tour_dict.get("dates")
            tour_dict["dates"] = sorted(dates, key=lambda d: d["date"]) if dates else []

        return tour_dict
