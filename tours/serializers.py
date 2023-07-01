from .models import Tour, TourUser
from rest_framework.exceptions import ValidationError
from bands.serializers import BandUserSerializer, serializers
from core.serializers import BaseSerializer
from datetime import datetime


class TourUserSerializer(BaseSerializer):
    class Meta:
        model = TourUser
        fields = "id", "banduser_id", "email", "username", "is_admin"

    email = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    is_admin = serializers.SerializerMethodField()

    def get_email(self, touruser: TourUser):
        return touruser.banduser.user.email

    def get_username(self, touruser: TourUser):
        return touruser.banduser.user.username

    def get_is_admin(self, touruser: TourUser):
        return touruser.banduser.is_admin

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
        fields = ("id", "name", "is_archived", "band_id", "tour_users", "dates")

    tour_users = TourUserSerializer(source="tourusers", read_only=True, many=True)
    dates = serializers.SerializerMethodField()

    def get_dates(self, tour: Tour):
        dates = tour.dates.all().order_by("date")
        if not self.past_dates:
            dates = dates.filter(date__gte=datetime.now().date())
        return DateSerializer(dates, many=True, context=self.context).data

    def create(self, validated_data: dict):
        validated_data["band_id"] = self.context.get("band_id")
        duplicate = Tour.objects.filter(band_id=validated_data.get("band_id"), name=validated_data.get("name")).first()
        if duplicate:
            raise ValidationError({"details": "Cannot have duplicate tours.", "code": "DUPLICATE"})
        return super().create(validated_data)

    def get_fields(self):
        fields = super().get_fields()
        if self.include not in ["dates", "all"]:
            fields.pop("dates")
        return fields

    def init_query_params(self):
        self.past_dates = False
        self.include = ""


class ToursSerializer(TourSerializer):
    many = True

    def init_query_params(self):
        super().init_query_params()
        self.archived_tours = False
