from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from .serializers import Venue, VenueSerializer, VenueNote
from core.permissions import IsVerified
from bands.permissions import IsBandAdmin, IsBandUser, IsBandOwner
from core.views import BaseAPIView
from core.query_params import BooleanQueryParam, ListQueryParam, QueryParam
from django.db.models import Q


class VenueCollectionView(generics.ListCreateAPIView, BaseAPIView):
    serializer_class = VenueSerializer
    permission_classes = (IsVerified,)

    def get_queryset(self):
        venues = Venue.objects.filter(Q(is_public=True) | Q(creator=self.request.user)).order_by("place__name")
        return venues


class VenueView(generics.RetrieveUpdateAPIView, BaseAPIView):
    serializer_class = VenueSerializer
    permission_classes = (IsVerified,)
    lookup_field = "id"
    lookup_url_kwarg = "venue_id"

    def get_queryset(self):
        venues = Venue.objects.filter(Q(is_public=True) | Q(creator=self.request.user)).order_by("place__name")
        return venues
