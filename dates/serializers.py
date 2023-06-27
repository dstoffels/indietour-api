from rest_framework import serializers
from .models import Date
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404


class DateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Date
        fields = ("id", "date", "notes", "is_show_day", "is_confirmed", "title", "tour_id")
