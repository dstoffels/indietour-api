from .models import Venue, VenueNote
from places.serializers import PlaceSerializer
from bands.serializers import BandUserSerializer, serializers
from core.serializers import BaseSerializer
from core.query_params import QueryParam, ListQueryParam
from datetime import date
from prospects.serializers import ProspectSerializer


class VenueSerializer(BaseSerializer):
    class Meta:
        model = Venue
        fields = "id", "place", "creator", "is_public", "capacity", "type", "place_id"

    place = PlaceSerializer(read_only=True)
    place_id = serializers.CharField(write_only=True)
