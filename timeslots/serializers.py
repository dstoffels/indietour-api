from rest_framework import serializers
from .models import Timeslot
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from places.utils import fetch_place
from places.serializers import PlaceSerializer
from core.serializers import BaseSerializer


class TimeslotSerializer(BaseSerializer):
    class Meta:
        model = Timeslot
        fields = (
            "id",
            "title",
            "details",
            "type",
            "start_time",
            "origin_id",
            "origin",
            "start_after_midnight",
            "end_time",
            "destination_id",
            "destination",
            "end_after_midnight",
        )

    title = serializers.CharField(required=True)
    type = serializers.ChoiceField(choices=Timeslot.TYPES, required=True)
    start_time = serializers.TimeField(required=True, format="%H:%M")
    origin_id = serializers.CharField(write_only=True, required=False, allow_null=True)
    origin = PlaceSerializer(read_only=True)
    end_time = serializers.TimeField(required=False, format="%H:%M")
    destination = PlaceSerializer(read_only=True)
    destination_id = serializers.CharField(write_only=True, required=False, allow_null=True)

    def create(self, validated_data: dict):
        validated_data["date_id"] = self.path_vars.date_id
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
