from rest_framework import generics
from rest_framework.request import Request
from .serializers import Lodging, LodgingSerializer
from tours.permissions import IsTourUser, IsTourAdmin
from core.views import BaseAPIView
from core.query_params import ListQueryParam, BooleanQueryParam, QueryParam
from datetime import date


class LodgingsView(generics.ListCreateAPIView, BaseAPIView):
    serializer_class = LodgingSerializer

    def get_queryset(self):
        return Lodging.objects.filter(date_id=self.path_vars.date_id)

    def get_permissions(self):
        if self.request.method == "GET":
            return (IsTourUser(),)
        return (IsTourAdmin(),)


class LodgingView(generics.RetrieveUpdateDestroyAPIView, BaseAPIView):
    serializer_class = LodgingSerializer
    lookup_field = "id"
    lookup_url_kwarg = "lodging_id"

    def get_queryset(self):
        return Lodging.objects.filter(date_id=self.path_vars.date_id)

    def get_permissions(self):
        if self.request.method == "GET":
            return (IsTourUser(),)
        return (IsTourAdmin(),)
