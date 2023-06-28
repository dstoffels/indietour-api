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
