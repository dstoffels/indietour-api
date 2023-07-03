from rest_framework import serializers
from .models import Prospect, LogEntry
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from places.utils import fetch_place
from places.serializers import PlaceSerializer
from core.serializers import BaseSerializer


class LogEntrySerializer(BaseSerializer):
    class Meta:
        model = LogEntry
        fields = "id", "timestamp", "note"

        timestamp = serializers.DateTimeField(read_only=True)
        note = serializers.CharField()


class ProspectSerializer(BaseSerializer):
    class Meta:
        model = Prospect
        fields = "id", "place", "notes", "status", "hold", "log", "place_id"

    place = PlaceSerializer(read_only=True)
    place_id = serializers.CharField(write_only=True)
    notes = serializers.CharField(required=False)
    status = serializers.ChoiceField(choices=Prospect.STATUS_CHOICES, default=Prospect.STATUS_CHOICES[0])
    hold = serializers.IntegerField(required=False)
    log = LogEntrySerializer(many=True, read_only=True, required=False)

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
