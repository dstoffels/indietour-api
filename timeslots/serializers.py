from rest_framework import serializers
from .models import Timeslot
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from places.utils import fetch_place
from places.serializers import PlaceSerializer


class TimeslotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timeslot
        exclude = ["date"]

    start_time = serializers.TimeField(required=True)
    date_id = serializers.UUIDField(write_only=True, required=False)
    origin_id = serializers.CharField(write_only=True, required=False)
    destination_id = serializers.CharField(write_only=True, required=False)
    origin = PlaceSerializer(read_only=True)
    destination = PlaceSerializer(read_only=True)
    type_options = serializers.SerializerMethodField()

    def get_type_options(self, timeslot):
        return Timeslot.TYPES

    def create(self, validated_data):
        validated_data["date_id"] = self.context.get("date_id")
        origin_id = validated_data.get("origin_id")
        if origin_id:
            validated_data["origin"] = self._new_place(origin_id)

        destination_id = validated_data.get("destination_id")
        if destination_id:
            validated_data["destination"] = self._new_place(destination_id)

        return super().create(validated_data)

    def update(self, instance, validated_data):
        origin_id = validated_data.get("origin_id")
        if origin_id:
            validated_data["origin"] = self._new_place(origin_id)

        destination_id = validated_data.get("destination_id")
        if destination_id:
            validated_data["destination"] = self._new_place(destination_id)

        return super().update(instance, validated_data)

    def _new_place(self, place_id):
        ser = PlaceSerializer(data={"place_id": place_id})
        ser.is_valid()
        ser.save()
        return ser.instance

    def is_valid(self, *, raise_exception=True):
        from tours.models import Tour
        from dates.models import Date

        band_id = self.context.get("band_id")
        tour_id = self.context.get("tour_id")
        date_id = self.context.get("date_id")
        tour = get_object_or_404(Tour, id=tour_id)
        date = get_object_or_404(Date, id=date_id)

        if str(tour.band_id) != band_id:
            raise ValidationError({"details": "Tour does no belong to this Band.", "code": "INVALID"})
        if str(date.tour_id) != tour_id:
            raise ValidationError({"details": "Date does no belong to this Tour.", "code": "INVALID"})

        return super().is_valid(raise_exception=raise_exception)
