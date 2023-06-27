from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from authentication.models import User
from bands.models import Band
from .serializers import Tour, TourSerializer, TourUser, TourUserSerializer
from .permissions import IsTourUser, IsTourAdmin
from bands.permissions import IsBandAdmin
from itertools import chain
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404


class ToursView(generics.ListCreateAPIView):
    serializer_class = TourSerializer
    permission_classes = (IsBandAdmin,)

    def perform_create(self, serializer: TourSerializer):
        user: User = self.request.user
        serializer.save(band_id=self.kwargs.get("band_id"))
        user.active_tour = serializer.instance
        return super().perform_create(serializer)

    def get_queryset(self):
        return Tour.objects.filter(band_id=self.kwargs.get("band_id"))


class TourView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    lookup_field = "id"
    lookup_url_kwarg = "tour_id"

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsTourUser()]
        return [IsTourAdmin()]


class TourUsersView(generics.CreateAPIView):
    queryset = TourUser.objects.all()
    permission_classes = (IsTourAdmin,)
    serializer_class = TourUserSerializer

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        tour = get_object_or_404(Tour, id=self.kwargs.get("tour_id"))
        return Response(TourSerializer(tour).data)

    def perform_create(self, serializer):
        serializer.initial_data["band_id"] = self.kwargs.get("band_id")
        serializer.save(tour_id=self.kwargs.get("tour_id"))
        return super().perform_create(serializer)


class TourUserView(generics.DestroyAPIView):
    queryset = TourUser.objects.all()
    permission_classes = (IsTourAdmin,)
    serializer_class = TourUserSerializer
    lookup_url_kwarg = "touruser_id"
    lookup_field = "id"

    def delete(self, request, *args, **kwargs):
        tour = self.get_object().tour
        super().delete(request, *args, **kwargs)
        return Response(TourSerializer(tour).data, 204)
