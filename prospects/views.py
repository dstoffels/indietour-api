from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from .serializers import Prospect, ProspectSerializer, LogEntry, LogEntrySerializer
from tours.permissions import IsTourUser, IsTourAdmin
from core.views import BaseAPIView
from core.query_params import ListQueryParam, BooleanQueryParam, QueryParam
from datetime import date
from dates.serializers import Date, DateSerializer
from django.forms.models import model_to_dict


class ProspectsView(generics.ListCreateAPIView, BaseAPIView):
    serializer_class = ProspectSerializer
    permission_classes = (IsTourAdmin,)

    def get_queryset(self):
        return Prospect.objects.filter(tour_id=self.path_vars.tour_id).order_by("date")


class ProspectView(generics.RetrieveUpdateDestroyAPIView, generics.CreateAPIView, BaseAPIView):
    serializer_class = ProspectSerializer
    permission_classes = (IsTourAdmin,)
    lookup_field = "id"
    lookup_url_kwarg = "prospect_id"

    def get_queryset(self):
        return Prospect.objects.filter(tour_id=self.path_vars.tour_id).order_by("date")


class LogView(generics.ListCreateAPIView, BaseAPIView):
    serializer_class = LogEntrySerializer
    permission_classes = (IsTourAdmin,)

    def get_queryset(self):
        return LogEntry.objects.filter(prospect_id=self.path_vars.prospect_id).order_by("timestamp")


class LogEntryView(generics.RetrieveUpdateDestroyAPIView, BaseAPIView):
    serializer_class = LogEntrySerializer
    permission_classes = (IsTourAdmin,)
    lookup_field = "id"
    lookup_url_kwarg = "logentry_id"

    def get_queryset(self):
        return LogEntry.objects.filter(prospect_id=self.path_vars.prospect_id).order_by("timestamp")


class ConfirmProspectView(generics.CreateAPIView, BaseAPIView):
    serializer_class = ProspectSerializer
    permission_classes = (IsTourAdmin,)
    lookup_field = ("id",)
    lookup_url_kwarg = "prospect_id"

    def post(self, request, *args, **kwargs):
        prospect = Prospect.objects.filter(id=self.path_vars.prospect_id).first()

        data = prospect.extract_date()

        ser = DateSerializer(data=data, context=self.get_serializer_context())
        ser.is_valid()
        ser.save()

        date: Date = ser.instance
        for placecontact in prospect.venue.place.contacts.filter(contact__owner=self.user):
            date.contacts.create(contact=placecontact.contact, title=placecontact.title)

        prospect.status = "CONFIRMED"
        prospect.confirmed_date_id = date.id
        prospect.save()

        return Response(ser.data, 201)
