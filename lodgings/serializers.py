from rest_framework import serializers
from .models import Lodging
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from places.utils import fetch_place
from places.serializers import PlaceSerializer
from core.serializers import BaseSerializer


class LodgingSerializer(BaseSerializer):
    class Meta:
        model = Lodging
        fields = "id", "place", "title", "notes", "place_id"

    place = PlaceSerializer(read_only=True)
    place_id = serializers.CharField(write_only=True)
    title = serializers.CharField(required=False)
    notes = serializers.CharField(required=False)

    def create(self, validated_data: dict):
        validated_data["date_id"] = self.path_vars.date_id
        self._set_place()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        self._set_place()
        return super().update(instance, validated_data)

    def _set_place(self):
        place_id = self.validated_data.get("place_id")
        if place_id:
            ser = PlaceSerializer(data={"place_id": place_id})
            ser.is_valid()
            ser.save()
            self.validated_data["place"] = ser.instance
