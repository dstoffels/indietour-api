from rest_framework import generics
from rest_framework.response import Response
from rest_framework.request import Request
from authentication.models import User
from .serializers import Place, PlaceSerializer
from authentication.permissions import IsVerified
from django.shortcuts import get_object_or_404
import requests
import os

BASE_URL = "https://maps.googleapis.com/maps/api"


class PlaceView(generics.RetrieveAPIView):
    permission_classes = (IsVerified,)
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    lookup_url_kwarg = "place_id"
    lookup_field = "id"

    def retrieve(self, request, *args, **kwargs):
        place_id = self.kwargs.get("place_id")
        ser = PlaceSerializer(data={"place_id": place_id})
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)


class AutocompleteView(generics.RetrieveAPIView):
    permission_classes = (IsVerified,)

    def get(self, request: Request, *args, **kwargs):
        input = request.GET.get("input")
        response = requests.get(
            f"{BASE_URL}/place/autocomplete/json?key={os.getenv('GOOGLE_API_KEY')}&input={input}&fields=geometry"
        )
        return Response(response.json())


class DirectionsView(generics.RetrieveAPIView):
    permission_classes = (IsVerified,)

    def get(self, request, *args, **kwargs):
        origin = request.GET.get("origin")
        destination = request.GET.get("destination")
        response = requests.get(
            f"{BASE_URL}/directions/json?key={os.getenv('GOOGLE_API_KEY')}&origin=place_id:{origin}&destination=place_id:{destination}"
        )
        return Response(response.json())
