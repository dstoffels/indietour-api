from rest_framework import serializers
from contacts.serializers import ContactSerializer
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from timeslots.serializers import TimeslotSerializer
from lodgings.serializers import LodgingSerializer
from places.serializers import PlaceSerializer, Place
from core.serializers import BaseSerializer
from core.query_params import BooleanQueryParam, ListQueryParam
from .models import Date, Show
from venues.serializers import Venue, VenueSerializer


class ShowSerializer(BaseSerializer):
    class Meta:
        model = Show
        fields = ("id", "venue", "venue_id", "deal", "hospitality", "notes", "date_id")

    venue = VenueSerializer(read_only=True)
    venue_id = serializers.UUIDField(write_only=True)

    def create(self, validated_data):
        validated_data["date_id"] = self.path_vars.date_id
        return super().create(validated_data)


class DateSerializer(BaseSerializer):
    class Meta:
        model = Date
        fields = (
            "id",
            "date",
            "place",
            "place_id",
            "title",
            "notes",
            "status",
            "hold",
            "shows",
            "timeslots",
            "lodgings",
            "contacts",
            "tour_id",
        )

    place = PlaceSerializer(read_only=True)
    place_id = serializers.CharField(write_only=True)
    shows = ShowSerializer(read_only=True, many=True)
    timeslots = TimeslotSerializer(read_only=True, many=True)
    lodgings = LodgingSerializer(read_only=True, many=True)
    contacts = ContactSerializer(read_only=True, many=True)

    def create(self, validated_data: dict):
        tour_id = self.path_vars.tour_id
        validated_data["tour_id"] = tour_id
        # duplicate = Date.objects.filter(tour_id=tour_id, date=validated_data.get("date")).first()
        # if duplicate:
        #     raise ValidationError({"details": "Cannot have duplicate dates in a tour.", "code": "DUPLICATE"})

        ser = PlaceSerializer(data=validated_data, context=self.context)
        ser.is_valid()
        ser.save()

        return super().create(validated_data)

    def update(self, instance, validated_data: dict):
        if validated_data.get("place_id"):
            ser = PlaceSerializer(data=validated_data, context=self.context)
            ser.is_valid()
            ser.save()
        return super().update(instance, validated_data)

    def init_query_params(self):
        self.include: ListQueryParam
        self.past_dates: BooleanQueryParam

    def get_fields(self):
        fields = super().get_fields()
        if not self.include.contains("all"):
            if not self.include.contains("timeslots"):
                fields.pop("timeslots")
            if not self.include.contains("lodgings"):
                fields.pop("lodgings")
            if not self.include.contains("contacts"):
                fields.pop("contacts")

        return fields
