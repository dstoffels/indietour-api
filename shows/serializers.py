from rest_framework import serializers
from django.shortcuts import get_object_or_404
from core.serializers import BaseSerializer
from core.query_params import BooleanQueryParam, ListQueryParam
from .models import Show, LogEntry
from venues.serializers import Venue, VenueSerializer
from core.utils import retrieve_or_404


class LogEntrySerializer(BaseSerializer):
    parent_url_kwarg = "show_id"

    class Meta:
        model = LogEntry
        fields = "id", "timestamp", "note"


class ShowSerializer(BaseSerializer):
    class Meta:
        model = Show
        fields = (
            "id",
            "venue",
            "venue_id",
            "status",
            "hold",
            "deal",
            "hospitality",
            "notes",
            "date_id",
            "log",
        )

    venue = VenueSerializer(read_only=True)
    venue_id = serializers.UUIDField(write_only=True)
    log = serializers.SerializerMethodField()

    def get_log(self, show: Show):
        return show.log.filter(show_id=show.id)

    def create(self, validated_data: dict):
        validated_data["date_id"] = self.path_vars.date_id
        retrieve_or_404(Venue, validated_data.get("venue_id"))
        return super().create(validated_data)
