from rest_framework import generics
from rest_framework.request import Request
from .serializers import Prospect, ProspectSerializer, LogEntry, LogEntrySerializer
from tours.permissions import IsTourUser, IsTourAdmin
from core.views import BaseAPIView
from core.query_params import ListQueryParam, BooleanQueryParam, QueryParam
from datetime import date


class ProspectsView(generics.ListCreateAPIView, BaseAPIView):
    serializer_class = ProspectSerializer

    def get_queryset(self):
        return Prospect.objects.filter(date_id=self.path_vars.date_id)
