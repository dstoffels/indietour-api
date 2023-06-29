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
from core.views import DateDependentView


class TimeslotsView(generics.CreateAPIView, DateDependentView):
    serializer_class = TimeslotSerializer
    permission_classes = (IsTourAdmin,)

    def post(self, request: Request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return self.tour_response(201)


class TimeslotView(generics.RetrieveUpdateDestroyAPIView, DateDependentView):
    queryset = Timeslot.objects.all()
    serializer_class = TimeslotSerializer
    permission_classes = (IsTourAdmin,)
    lookup_url_kwarg = "timeslot_id"
    lookup_field = "id"

    def patch(self, request, *args, **kwargs):
        super().patch(request, *args, **kwargs)
        return self.tour_response()

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return self.tour_response()
