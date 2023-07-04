from rest_framework import generics
from rest_framework.response import Response
from rest_framework.request import Request
from authentication.models import User
from .serializers import Place, PlaceSerializer
from core.permissions import IsVerified
from core.views import BaseAPIView
from django.shortcuts import get_object_or_404
import requests
import os
from .utils import GAPI_BASE_URL
from core.query_params import QueryParam


class PlaceView(generics.RetrieveAPIView, BaseAPIView):
    permission_classes = (IsVerified,)
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    lookup_url_kwarg = "place_id"
    lookup_field = "id"


class AutocompleteView(generics.RetrieveAPIView, BaseAPIView):
    permission_classes = (IsVerified,)

    def get(self, request: Request, *args, **kwargs):
        input = request.GET.get("input")
        response = requests.get(
            f"{GAPI_BASE_URL}/place/autocomplete/json?key={os.getenv('GOOGLE_API_KEY')}&input={input}&fields=geometry"
        )
        return Response(response.json())


class DirectionsView(generics.RetrieveAPIView, BaseAPIView):
    permission_classes = (IsVerified,)

    def get_query_params(self):
        return [QueryParam("origin"), QueryParam("destination")]

    def get(self, request, *args, **kwargs):
        origin = self.query_params.get("origin").value
        destination = self.query_params.get("destination").value
        response = requests.get(
            f"{GAPI_BASE_URL}/directions/json?key={os.getenv('GOOGLE_API_KEY')}&origin=place_id:{origin}&destination=place_id:{destination}"
        )
        return Response(response.json())


class SearchView(generics.RetrieveAPIView, BaseAPIView):
    permission_classes = (IsVerified,)

    def get_query_params(self):
        return [QueryParam("query")]

    def get(self, request, *args, **kwargs):
        query = self.query_params.get("query").value
        response = requests.get(
            f"{GAPI_BASE_URL}/place/textsearch/json?key={os.getenv('GOOGLE_API_KEY')}&inputtype=textquery&query={query}keyword=music"
        )
        return Response(response.json())
