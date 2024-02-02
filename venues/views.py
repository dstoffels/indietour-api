from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from .serializers import Venue, VenueSerializer, VenueNote, VenueNoteSerializer
from core.permissions import IsVerified
from .permissions import IsVenueOwner, IsPublicVenue, IsNoteOwner
from core.views import BaseAPIView
from core.query_params import BooleanQueryParam, ListQueryParam, QueryParam
from django.db.models import Q
from contacts.models import Contact
import re


class VenueCollectionView(generics.ListCreateAPIView, BaseAPIView):
    serializer_class = VenueSerializer
    permission_classes = (IsVerified,)

    def get_queryset(self):
        venues = Venue.objects.filter(Q(public=True) | Q(creator=self.request.user))

        query = self.q.value
        if query:
            words = re.findall(r"\w+", query)
            query = Q()

            for word in words:
                query |= Q(place__name__icontains=word) | Q(
                    place__formatted_address__icontains=word
                )

            venues = venues.filter(query)
        if self.capacity.value:
            venues = venues.filter(capacity__lte=self.capacity.value)
        if self.type.value:
            venues = venues.filter(type=self.type.value)

        return venues

    def get_query_params(self):
        return [
            QueryParam("q"),
            QueryParam("name"),
            QueryParam("location"),
            QueryParam("capacity"),
            QueryParam("type"),
        ]

    def init_query_params(self, request: Request):
        super().init_query_params(request)

        self.q: QueryParam
        self.name: QueryParam
        self.location: QueryParam
        self.capacity: QueryParam
        self.type: QueryParam


class VenueView(generics.RetrieveUpdateDestroyAPIView, BaseAPIView):
    model = Venue
    serializer_class = VenueSerializer
    permission_classes = (IsPublicVenue,)
    lookup_field = "id"
    lookup_url_kwarg = "venue_id"

    # def get_queryset(self):
    #     venues = Venue.objects.filter(Q(public=True) | Q(creator=self.request.user)).order_by("place__name")
    #     return venues

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
    model = VenueNote
    serializer_class = VenueNoteSerializer
    permission_classes = (IsVerified,)
    lookup_field = "id"
    lookup_url_kwarg = "venuenote_id"


class VenueTypesView(generics.RetrieveAPIView, BaseAPIView):
    def get(self, request, *args, **kwargs):
        return Response(Venue.VENUE_TYPES)


class VenueContactView(generics.CreateAPIView, generics.DestroyAPIView, BaseAPIView):
    def post(self, request, *args, **kwargs):
        venue = Venue.objects.get(id=self.path_vars.venue_id)
        contact = Contact.objects.get(id=self.path_vars.contact_id)
        if not venue.contacts.contains(contact):
            venue.contacts.add(contact)
        return Response(
            VenueSerializer(venue, context=self.get_serializer_context()).data, 201
        )

    def delete(self, request, *args, **kwargs):
        venue = Venue.objects.get(id=self.path_vars.venue_id)
        contact = Contact.objects.get(id=self.path_vars.contact_id)
        if venue.contacts.contains(contact):
            venue.contacts.remove(contact)
        return Response(
            VenueSerializer(venue, context=self.get_serializer_context()).data, 200
        )
