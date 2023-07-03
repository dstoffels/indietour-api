from rest_framework import generics
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import ValidationError
from .serializers import Timeslot, TimeslotSerializer
from tours.serializers import Tour, TourSerializer
from dates.serializers import Date, DateSerializer
from tours.permissions import IsTourUser, IsTourAdmin, IsBandUser
from bands.permissions import IsBandAdmin
from django.shortcuts import get_object_or_404
from core.views import BaseAPIView


class TimeslotsView(generics.ListCreateAPIView, BaseAPIView):
    serializer_class = TimeslotSerializer
    permission_classes = (IsTourAdmin,)

    def get_queryset(self):
        return Timeslot.objects.filter(date_id=self.path_vars.date_id)


class TimeslotView(generics.RetrieveUpdateDestroyAPIView, BaseAPIView):
    queryset = Timeslot.objects.all()
    serializer_class = TimeslotSerializer
    permission_classes = (IsTourAdmin,)
    lookup_url_kwarg = "timeslot_id"
    lookup_field = "id"


class TimeslotTypeChoicesView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        return Response(Timeslot.TYPES)
