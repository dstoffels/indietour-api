from rest_framework import generics
from rest_framework.response import Response
from authentication.models import User
from .serializers import Timeslot, TimeslotSerializer
from tours.permissions import IsTourUser, IsTourAdmin, IsBandUser
from bands.permissions import IsBandAdmin
from django.shortcuts import get_object_or_404


class TimeslotsView(generics.CreateAPIView):
    serializer_class = TimeslotSerializer
    permission_classes = (IsTourAdmin,)

    def perform_create(self, serializer: TimeslotSerializer):
        date_id = self.kwargs.get("date_id")
        serializer.save(date_id=date_id)
        return super().perform_create(serializer)
