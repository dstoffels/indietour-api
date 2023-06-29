from rest_framework import generics
from rest_framework.response import Response
from bands.serializers import Band, BandSerializer
from .serializers import Tour, TourSerializer, TourUser, TourUserSerializer
from .permissions import IsTourUser, IsTourAdmin, IsBandUser
from bands.permissions import IsBandAdmin
from django.shortcuts import get_object_or_404
from core.views import BaseAPIView, BandDependentView, TourDependentView


class ToursView(generics.ListCreateAPIView, BaseAPIView):
    serializer_class = TourSerializer

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        band = get_object_or_404(Band, id=kwargs.get("band_id"))
        return Response(BandSerializer(band).data, 201)

    def get_queryset(self):
        return Tour.objects.filter(band_id=self.band_id)

    def get_permissions(self):
        if self.request.method == "GET":
            return (IsBandUser(),)
        return (IsBandAdmin(),)

    def initial(self, request, *args, **kwargs):
        self.band_id = self.kwargs.get("band_id")
        return super().initial(request, *args, **kwargs)


class TourView(generics.RetrieveUpdateDestroyAPIView, BandDependentView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    lookup_field = "id"
    lookup_url_kwarg = "tour_id"

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsTourUser()]
        return [IsTourAdmin()]


class TourUsersView(generics.CreateAPIView, TourDependentView):
    queryset = TourUser.objects.all()
    permission_classes = (IsTourAdmin,)
    serializer_class = TourUserSerializer

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        tour = get_object_or_404(Tour, id=self.kwargs.get("tour_id"))
        return Response(TourSerializer(tour).data, 201)


class TourUserView(generics.DestroyAPIView, TourDependentView):
    queryset = TourUser.objects.all()
    permission_classes = (IsTourAdmin,)
    serializer_class = TourUserSerializer
    lookup_url_kwarg = "touruser_id"
    lookup_field = "id"

    def delete(self, request, *args, **kwargs):
        tour = self.get_object().tour
        super().delete(request, *args, **kwargs)
        return Response(TourSerializer(tour).data, 204)
