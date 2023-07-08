from rest_framework import serializers
from django.shortcuts import get_object_or_404
from core.serializers import BaseSerializer
from core.query_params import BooleanQueryParam, ListQueryParam
from .models import Show
from venues.serializers import Venue, VenueSerializer


class ShowSerializer(BaseSerializer):
    class Meta:
        model = Show
        fields = ("id", "venue", "venue_id", "deal", "hospitality", "notes", "date_id")

    venue = VenueSerializer(read_only=True)
    venue_id = serializers.UUIDField(write_only=True)

    def create(self, validated_data):
        validated_data["date_id"] = self.path_vars.date_id
        return super().create(validated_data)
