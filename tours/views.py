from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from authentication.models import User
from bands.models import Band
from .serializers import Tour, TourSerializer, TourUser, TourUserSerializer
from bands.permissions import IsBandUser, IsBandAdmin, IsVerified
from itertools import chain
from django.shortcuts import get_object_or_404


class ToursView(generics.ListCreateAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    permission_classes = (IsBandUser,)

    def perform_create(self, serializer: TourSerializer):
        serializer.save(band_id=self.kwargs.get("band_id"))
        return super().perform_create(serializer)
