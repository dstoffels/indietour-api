from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from authentication.models import User
from .serializers import Date, DateSerializer
from tours.permissions import IsTourUser, IsTourAdmin
from bands.permissions import IsBandAdmin
from itertools import chain
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from tours.serializers import TourSerializer, Tour
from core.views import TourDependentView, BandDependentView
from core.query_params import ListQueryParam, BooleanQueryParam, QueryParam
from datetime import date


class BaseDatesView(BandDependentView):
    def get_query_params(self) -> list[QueryParam]:
        return [
            ListQueryParam("include", ["all", "timeslots", "contacts", "prospects", "lodgings"]),
            BooleanQueryParam("past_dates"),
        ]


class DatesView(generics.ListCreateAPIView, BaseDatesView):
    serializer_class = DateSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return (IsTourUser(),)
        return (IsTourAdmin(),)

    def get_queryset(self):
        tourdates = Date.objects.filter(tour_id=self.kwargs.get("tour_id")).order_by("date")
        if self.past_dates.is_invalid():
            tourdates = tourdates.filter(date__gte=date.today())
        return tourdates

    def init_query_params(self, request: Request):
        super().init_query_params(request)
        self.include: ListQueryParam
        self.past_dates: BooleanQueryParam


class DateView(generics.RetrieveUpdateDestroyAPIView, TourDependentView, BaseDatesView):
    queryset = Date.objects.all()
    serializer_class = DateSerializer
    lookup_field = "id"
    lookup_url_kwarg = "date_id"

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsTourUser()]
        return [IsTourAdmin()]
