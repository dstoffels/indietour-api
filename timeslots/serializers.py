from rest_framework import serializers
from .models import Timeslot
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from places.utils import fetch_place
from places.serializers import PlaceSerializer


class TimeslotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timeslot
        exclude = ("date",)

    # type_options = serializers.ListField(source=Timeslot.TYPES)
    date_id = serializers.DateField(write_only=True, required=False)
    origin_id = serializers.CharField(write_only=True, required=False)
    destination_id = serializers.CharField(write_only=True, required=False)
    origin = PlaceSerializer()

    def create(self, validated_data):
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
