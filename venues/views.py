from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from .serializers import Venue, VenueSerializer, VenueNote, VenueNoteSerializer
from core.permissions import IsVerified
from .permissions import IsVenueOwner, IsPublicVenue, IsNoteOwner
from core.views import BaseAPIView
from core.query_params import BooleanQueryParam, ListQueryParam, QueryParam
from django.db.models import Q


class VenueCollectionView(generics.ListCreateAPIView, BaseAPIView):
    serializer_class = VenueSerializer
    permission_classes = (IsVerified,)

    def get_queryset(self):
        venues = Venue.objects.filter(Q(is_public=True) | Q(creator=self.request.user)).order_by("place__name")
        if self.query.is_valid():
            if self.search_by.is_valid():
                return venues.filter(**{self.search_by.value: self.query.value})
            venues = venues.filter(
                Q(place__name__icontains=self.query.value) | Q(place__formatted_address__icontains=self.query.value)
            )
        return venues

    def get_query_params(self):
        return [QueryParam("query"), QueryParam("search_by", ["capacity", "type"])]

    def init_query_params(self, request: Request):
        super().init_query_params(request)
        self.query: QueryParam
        self.search_by: QueryParam


class VenueView(generics.RetrieveUpdateDestroyAPIView, BaseAPIView):
    serializer_class = VenueSerializer
    permission_classes = (IsPublicVenue,)
    lookup_field = "id"
    lookup_url_kwarg = "venue_id"

    def get_queryset(self):
        venues = Venue.objects.filter(Q(is_public=True) | Q(creator=self.request.user)).order_by("place__name")
        return venues

    def get_permissions(self):
        if self.request.method != "GET":
            return (IsVenueOwner(),)
        return super().get_permissions()


class VenueNotesView(generics.ListCreateAPIView, BaseAPIView):
    serializer_class = VenueNoteSerializer
    permission_classes = (IsVerified,)

    def get_queryset(self):
        return VenueNote.objects.filter(venue_id=self.path_vars.venue_id)


class VenueNoteView(generics.RetrieveUpdateDestroyAPIView, BaseAPIView):
    serializer_class = VenueNoteSerializer
    permission_classes = (IsVerified,)
    lookup_field = "id"
    lookup_url_kwarg = "venuenote_id"

    def get_queryset(self):
        return VenueNote.objects.filter(venue_id=self.path_vars.venue_id)
