from .models import Venue, VenueNote
from places.serializers import PlaceSerializer
from bands.serializers import BandUserSerializer, serializers
from places.models import Place
from core.serializers import BaseSerializer
from core.query_params import QueryParam, ListQueryParam
from datetime import date
from rest_framework.exceptions import ValidationError
from contacts.serializers import ContactSerializer


class VenueNoteSerializer(BaseSerializer):
    class Meta:
        model = VenueNote
        fields = "id", "user", "note"

    user = serializers.SerializerMethodField()

    def get_user(self, note: VenueNote):
        return note.user.username

    def create(self, validated_data):
        exisiting_note = VenueNote.objects.filter(user=self.user).first()
        if exisiting_note:
            raise ValidationError(
                {"detail": "Only one venue note allowed per user.", "code": "DUPLICATE"}
            )
        validated_data["venue_id"] = self.path_vars.venue_id
        validated_data["user"] = self.user
        return super().create(validated_data)


class VenueSerializer(BaseSerializer):
    class Meta:
        model = Venue
        fields = (
            "id",
            "place",
            "creator",
            "capacity",
            "type",
            "place_id",
            "note",
            "public",
            "contacts",
            "show_count",
        )

    place = PlaceSerializer(read_only=True)
    place_id = serializers.CharField(write_only=True)
    type = serializers.CharField(required=False, default="Other")
    capacity = serializers.IntegerField(required=False, default=0)
    creator = serializers.SerializerMethodField()
    contacts = serializers.SerializerMethodField()

    def get_contacts(self, venue: Venue):
        return ContactSerializer(
            venue.contacts.filter(owner=self.user), many=True, context=self.context
        ).data

    show_count = serializers.SerializerMethodField()

    def get_show_count(self, venue: Venue):
        return venue.shows.count()

    note = serializers.SerializerMethodField()

    def get_note(self, venue: Venue):
        note = venue.notes.filter(user=self.user).first()
        return VenueNoteSerializer(note, context=self.context).data

    def get_creator(self, venue: Venue):
        return venue.creator.username

    def create(self, validated_data: dict):
        place_id = validated_data.get("place_id")

        place = self._get_place(place_id)
        self.validate_place(place, validated_data)

        validated_data["place"] = place
        validated_data["creator"] = self.user

        return super().create(validated_data)

    def update(self, instance: Venue, validated_data: dict):
        self.validate_place(instance.place, validated_data)

        place_id = validated_data.get("place_id")

        if place_id:
            place = self._get_place(place_id)
            validated_data["place"] = place
            self.validate_place(place, validated_data)

        return super().update(instance, validated_data)

    def _get_place(self, place_id):
        ser = PlaceSerializer(data={"place_id": place_id}, context=self.context)
        ser.is_valid()
        ser.save()
        return ser.instance

    def validate_place(self, place: Place, validated_data: dict):
        if "premise" in place.types:
            validated_data["public"] = False
        elif "establishment" in place.types:
            validated_data["public"] = True
