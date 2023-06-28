from rest_framework import serializers
from .models import Date
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from timeslots.serializers import TimeslotSerializer


class DateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Date
        fields = ("id", "date", "notes", "is_show_day", "is_confirmed", "title", "tour_id", "timeslots")

    timeslots = TimeslotSerializer(read_only=True, many=True)

    def create(self, validated_data):
        duplicate = Date.objects.filter(tour_id=validated_data.get("tour_id"), date=validated_data.get("date")).first()
        if duplicate:
            raise ValidationError({"details": "Cannot have duplicate dates in a tour.", "code": "DUPLICATE"})
        return super().create(validated_data)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        timeslots = rep["timeslots"]
        rep["timeslots"] = sorted(timeslots, key=lambda d: d["start_time"])
        return rep
