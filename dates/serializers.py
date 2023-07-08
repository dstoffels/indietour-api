from rest_framework import serializers
from contacts.serializers import ContactSerializer
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from timeslots.serializers import TimeslotSerializer
from lodgings.serializers import LodgingSerializer
from places.serializers import PlaceSerializer, Place
from core.serializers import BaseSerializer
from core.query_params import BooleanQueryParam, ListQueryParam
from .models import Date, LogEntry
from shows.serializers import ShowSerializer


class LogEntrySerializer(BaseSerializer):
    parent_url_kwarg = "date_id"

    class Meta:
        model = LogEntry
        fields = "id", "timestamp", "note"


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
            if not self.include.contains("shows"):
                fields.pop("shows")
            if not self.include.contains("timeslots"):
                fields.pop("timeslots")
            if not self.include.contains("lodgings"):
                fields.pop("lodgings")
            if not self.include.contains("contacts"):
                fields.pop("contacts")

        return fields
