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
from core.views import TourDependentView


class DatesView(generics.ListCreateAPIView, TourDependentView):
    serializer_class = DateSerializer

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return self.tour_response(201)

    def get_queryset(self):
        return Date.objects.filter(tour_id=self.kwargs.get("tour_id"))

    def get_permissions(self):
        if self.request.method == "GET":
            return (IsTourUser(),)
        return (IsTourAdmin(),)


class DateView(generics.RetrieveUpdateDestroyAPIView, TourDependentView):
    queryset = Date.objects.all()
    serializer_class = DateSerializer
    lookup_field = "id"
    lookup_url_kwarg = "date_id"

    def patch(self, request, *args, **kwargs):
        super().patch(request, *args, **kwargs)
        return self.tour_response()

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return self.tour_response()

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsTourUser()]
        return [IsTourAdmin()]
