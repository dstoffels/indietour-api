from rest_framework import generics
from rest_framework.response import Response
from .serializers import Tour, TourSerializer, TourUser, TourUserSerializer
from .permissions import IsTourUser, IsTourAdmin, IsBandUser
from bands.permissions import IsBandAdmin
from core.views import BaseAPIView, BandDependentView, TourDependentView
from core.query_params import BooleanQueryParam, ListQueryParam, QueryParamsManager


class ToursView(generics.ListCreateAPIView, BaseAPIView):
    serializer_class = TourSerializer
    # query_params = QueryParamsManager(
    #     BooleanQueryParam("archived_tours"),
    #     ListQueryParam("include", ["all", "dates"]),
    #     BooleanQueryParam("past_dates"),
    # )

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return self.band_tours_response(201)

    def get_queryset(self):
        return self.get_tours_for_band()

    def get_permissions(self):
        if self.request.method == "GET":
            return (IsBandUser(),)
        return (IsBandAdmin(),)


class TourView(generics.RetrieveUpdateDestroyAPIView, BandDependentView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    lookup_field = "id"
    lookup_url_kwarg = "tour_id"
    # query_params = QueryParamsManager(ListQueryParam("include", ["all", "dates"]), BooleanQueryParam("past_dates"))

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
        return self.tour_response(201)


class TourUserView(generics.DestroyAPIView, TourDependentView):
    queryset = TourUser.objects.all()
    permission_classes = (IsTourAdmin,)
    serializer_class = TourUserSerializer
    lookup_url_kwarg = "touruser_id"
    lookup_field = "id"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return self.tour_response()
