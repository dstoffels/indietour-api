from typing import Any
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from bands.serializers import Band, BandSerializer
from tours.serializers import Tour, TourSerializer
from dates.serializers import Date, DateSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.request import Request
from django.db.models import Q
from .query_params import QueryParam, QueryParamsManager
from core.path_vars import PathVars


class BaseAPIView(generics.GenericAPIView):
    """Base for all indietour views.

    Path variables are automatically assigned to serializer context."""

    def initial(self, request, *args, **kwargs):
        self.path_vars = PathVars(kwargs)
        self.init_query_params(request)
        return super().initial(request, *args, **kwargs)

    def init_query_params(self, request: Request):
        """(OPTIONAL) Can be overridden to create instance vars for each query param. For intellisense only. Called in self.initial()

        Syntax: self.instance_variable: QueryParam (do not assign a value)"""
        self.query_params = QueryParamsManager(self.get_query_params(), request)
        self.query_params.to_obj_attrs(self)

    def get_query_params(self):
        """Must return a list of core.query_params.QueryParam. Called in self.initial() to set self.query_params"""
        return []

    def get_serializer_context(self):
        """Adds path variables and query params to serializer context dict. Query params are validated before being added."""
        context = super().get_serializer_context()
        context.update(self.kwargs)
        self.path_vars.update_context(context)
        self.query_params.update_context(context)
        return context

    def band_response(self, status_code=200):
        band = get_object_or_404(Band, id=self.path_vars.band_id)
        ser = BandSerializer(band, context=self.get_serializer_context())
        return Response(ser.data, status_code)

    def tour_response(self, status_code=200):
        tour = get_object_or_404(Tour, id=self.path_vars.tour_id)
        ser = TourSerializer(tour, context=self.get_serializer_context())
        return Response(ser.data, status_code)
