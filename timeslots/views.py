from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .serializers import Timeslot, TimeslotSerializer
from tours.serializers import Tour, TourSerializer
from dates.serializers import Date, DateSerializer
from tours.permissions import IsTourUser, IsTourAdmin, IsBandUser
from bands.permissions import IsBandAdmin
from django.shortcuts import get_object_or_404


class TimeslotsView(generics.CreateAPIView):
    serializer_class = TimeslotSerializer
    permission_classes = (IsTourAdmin,)

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return Response(TourSerializer(self.tour).data)

    def perform_create(self, serializer: TimeslotSerializer):
        date_id = self.kwargs.get("date_id")
        serializer.save(date_id=date_id)
        return super().perform_create(serializer)


class TimeslotView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Timeslot.objects.all()
    serializer_class = TimeslotSerializer
    permission_classes = (IsTourAdmin,)
    lookup_url_kwarg = "timeslot_id"
    lookup_field = "id"
