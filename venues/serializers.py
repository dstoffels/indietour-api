from .models import Venue, VenueNote
from places.serializers import PlaceSerializer
from bands.serializers import BandUserSerializer, serializers
from places.models import Place
from core.serializers import BaseSerializer
from core.query_params import QueryParam, ListQueryParam
from datetime import date
from prospects.serializers import ProspectSerializer
from rest_framework.exceptions import ValidationError


class VenueNoteSerializer(BaseSerializer):
    class Meta:
        models = VenueNote
        fields = "id", "user", "note"


class VenueSerializer(BaseSerializer):
    class Meta:
        model = Venue
        fields = "id", "place", "creator", "is_public", "capacity", "type", "place_id", "notes"

    place = PlaceSerializer(read_only=True)
    place_id = serializers.CharField(write_only=True)
    capacity = serializers.IntegerField(required=False, default=0)
    creator = serializers.SerializerMethodField()
    notes = VenueNoteSerializer(many=True, read_only=True)

    def get_creator(self, venue: Venue):
        return venue.creator.username

    def create(self, validated_data: dict):
        place_id = validated_data.get("place_id")

        self.validate_venue(place_id)

        place = self._get_place(place_id)
        self.validate_place(place, validated_data)

        validated_data["place"] = place
        validated_data["creator"] = self.user

        return super().create(validated_data)

    def update(self, instance: Venue, validated_data: dict):
        self.validate_place(instance.place, validated_data)

        place_id = validated_data.get("place_id")

        if place_id:
            self.validate_venue(place_id)
            place = self._get_place(place_id)
            validated_data["place"] = place
            self.validate_place(place, validated_data)

        return super().update(instance, validated_data)

    def validate_venue(self, place_id):
        existing_public_venue = Venue.objects.filter(place_id=place_id, is_public=True).first()
        if existing_public_venue:
            raise ValidationError({"detail": "This venue has already been published", "code": "INVALID"})

    def _get_place(self, place_id):
        ser = PlaceSerializer(data={"place_id": place_id})
        ser.is_valid()
        ser.save()
        return ser.instance

    def validate_place(self, place: Place, validated_data: dict):
        if "premise" in place.types:
            validated_data["is_public"] = False
        elif "establishment" in place.types:
            validated_data["is_public"] = True
