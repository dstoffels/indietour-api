from typing import Any
from rest_framework import generics
from bands.serializers import Band, BandSerializer
from tours.serializers import Tour, TourSerializer
from dates.serializers import Date, DateSerializer
from django.shortcuts import get_object_or_404
from core.utils import retrieve_or_404
from rest_framework.response import Response
from core.request import Request
from .query_params import QueryParam, QueryParamsManager
from core.path_vars import PathVars
from authentication.models import User
from core.models import UUIDModel


class BaseAPIView(generics.GenericAPIView):
    request: Request
    model: UUIDModel = None
    """Base for all indietour views.

    Path variables and query params automatically assigned to view and serializer."""

    def initial(self, request: Request, *args, **kwargs):
        self.user: User = request.user
        self.path_vars = PathVars(kwargs, request)
        self.init_query_params(request)
        return super().initial(request, *args, **kwargs)

    def init_query_params(self, request: Request):
        """(OPTIONAL) Can be overridden to create instance vars for each query param for easy access. Called in initial()

        Syntax: self.instance_variable: QueryParam (do not assign a value)"""
        self.query_params = QueryParamsManager(self.get_query_params(), request)
        self.query_params.to_obj_attrs(self)

    def get_query_params(self):
        """Must return a list of core.query_params.QueryParam.  Called in initial()"""
        return []

    def get_serializer_context(self):
        """Adds path variables and query params to serializer context dict. Query params are validated before being added."""
        context = super().get_serializer_context()
        context.update(self.kwargs)
        self.path_vars.update_context(context)
        self.query_params.update_context(context)
        return context

    def custom_response(self, model, serializer, id, status_code=200):
        obj = retrieve_or_404(model, id=id)
        ser = serializer(obj, context=self.get_serializer_context())
        return Response(ser.data, status_code)

    def band_response(self, status_code=200):
        return self.custom_response(Band, BandSerializer, self.path_vars.band_id, status_code)

    def tour_response(self, status_code=200):
        return self.custom_response(Tour, TourSerializer, self.path_vars.tour_id, status_code)

    def date_response(self, status_code=200):
        return self.custom_response(Date, DateSerializer, self.path_vars.date_id, status_code)

    def get_object(self):
        model_name = self.model.__name__.lower()
        id = self.request.kwargs.get(f"{model_name}_id")

        if hasattr(self.request, model_name):
            obj = getattr(self.request, model_name)
            return obj

        return retrieve_or_404(self.model, id)
