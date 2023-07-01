from rest_framework import serializers
from .models import Date
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from timeslots.serializers import TimeslotSerializer
from places.serializers import PlaceSerializer


class DateSerializer(serializers.ModelSerializer):
    include_timeslots = False
    include_prospect = False
    include_contacts = False

    class Meta:
        model = Date
        fields = ("id", "date", "title", "place", "place_id", "notes", "is_show_day", "is_confirmed", "timeslots")

    place = PlaceSerializer(read_only=True)
    place_id = serializers.CharField(write_only=True)
    timeslots = TimeslotSerializer(read_only=True, many=True)

    def create(self, validated_data):
        tour_id = self.context.get("tour_id")
        validated_data["tour_id"] = tour_id
        duplicate = Date.objects.filter(tour_id=tour_id, date=validated_data.get("date")).first()
        if duplicate:
            raise ValidationError({"details": "Cannot have duplicate dates in a tour.", "code": "DUPLICATE"})
        return super().create(validated_data)

    def to_representation(self, instance):
        date_dict = super().to_representation(instance)
        timeslots = date_dict["timeslots"]
        if not self.include_timeslots:
            date_dict.pop("timeslots")
        else:
            date_dict["timeslots"] = sorted(timeslots, key=lambda d: d["start_time"])
        return date_dict
