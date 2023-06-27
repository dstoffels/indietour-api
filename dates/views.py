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


class DatesView(generics.ListCreateAPIView):
    serializer_class = DateSerializer

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        tour = get_object_or_404(Tour, id=self.tour_id)
        return Response(TourSerializer(tour).data, 201)

    def perform_create(self, serializer: DateSerializer):
        serializer.save(tour_id=self.tour_id)
        return super().perform_create(serializer)

    def get_queryset(self):
        return Date.objects.filter(tour_id=self.tour_id)

    def get_permissions(self):
        if self.request.method == "GET":
            return (IsTourUser(),)
        return (IsTourAdmin(),)

    def initial(self, request, *args, **kwargs):
        self.tour_id = self.kwargs.get("tour_id")
        return super().initial(request, *args, **kwargs)


class DateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Date.objects.all()
    serializer_class = DateSerializer
    lookup_field = "id"
    lookup_url_kwarg = "date_id"

    def patch(self, request, *args, **kwargs):
        super().patch(request, *args, **kwargs)
        return Response(TourSerializer(self.tour).data)

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return Response(TourSerializer(self.tour).data)

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsTourUser()]
        return [IsTourAdmin()]

    def initial(self, request, *args, **kwargs):
        self.tour_id = self.kwargs.get("tour_id")
        self.tour = get_object_or_404(Tour, id=self.tour_id)
        return super().initial(request, *args, **kwargs)
