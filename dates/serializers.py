from rest_framework import serializers
from .models import Date
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from timeslots.serializers import TimeslotSerializer
from places.serializers import PlaceSerializer, Place
from core.serializers import BaseSerializer
from core.query_params import BooleanQueryParam, ListQueryParam


class DateSerializer(BaseSerializer):
    class Meta:
        model = Date
        fields = ("id", "date", "title", "place", "place_id", "notes", "is_show_day", "is_confirmed", "timeslots")

    place = PlaceSerializer(read_only=True)
    place_id = serializers.CharField(write_only=True)  # TODO: Do I want place_id to be required?
    timeslots = TimeslotSerializer(read_only=True, many=True)

    def create(self, validated_data: dict):
        tour_id = self.path_vars.tour_id
        validated_data["tour_id"] = tour_id
        duplicate = Date.objects.filter(tour_id=tour_id, date=validated_data.get("date")).first()
        if duplicate:
            raise ValidationError({"details": "Cannot have duplicate dates in a tour.", "code": "DUPLICATE"})

        ser = PlaceSerializer(data=validated_data)
        ser.is_valid()
        ser.save()

        return super().create(validated_data)

    def update(self, instance, validated_data):
        ser = PlaceSerializer(data=validated_data)
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
            # if not self.include.contains("prospects"):
            #     fields.pop("prospects")
            # if not self.include.contains("contacts"):
            #     fields.pop("contacts")
            # if not self.include.contains("lodgings"):
            #     fields.pop("lodgings")
        return fields
