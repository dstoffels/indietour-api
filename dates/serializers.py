from rest_framework import serializers
from contacts.serializers import ContactSerializer
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from timeslots.serializers import TimeslotSerializer, Timeslot
from lodgings.serializers import LodgingSerializer
from places.serializers import PlaceSerializer, Place
from core.serializers import BaseSerializer
from core.query_params import BooleanQueryParam, ListQueryParam
from .models import Date
from shows.serializers import ShowSerializer


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
            "is_published",
            "shows",
            "timeslots",
            "lodgings",
            "contacts",
            "tour_id",
            "is_show_day",
        )

    place = PlaceSerializer(read_only=True)
    place_id = serializers.CharField(write_only=True, required=False)
    shows = ShowSerializer(read_only=True, many=True)
    timeslots = serializers.SerializerMethodField()
    lodgings = LodgingSerializer(read_only=True, many=True)
    contacts = ContactSerializer(read_only=True, many=True)

    def get_timeslots(self, date):
        timeslots = Timeslot.objects.filter(date=date).order_by("start_time")
        return TimeslotSerializer(
            timeslots, read_only=True, many=True, context=self.context
        ).data

    def create(self, validated_data: dict):
        tour_id = self.path_vars.tour_id
        status = validated_data.get("status")
        validated_data["tour_id"] = tour_id
        duplicate = (
            status == "CONFIRMED"
            and Date.objects.filter(
                tour_id=tour_id, date=validated_data.get("date"), status="CONFIRMED"
            ).first()
        )
        if duplicate:
            raise ValidationError(
                {
                    "detail": "Cannot have duplicate dates in a tour.",
                    "code": "DUPLICATE",
                }
            )

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
