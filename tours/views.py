from rest_framework import generics
from rest_framework.response import Response
from .serializers import Tour, TourSerializer, TourUser, TourUserSerializer, ToursSerializer
from .permissions import IsTourUser, IsTourAdmin, IsBandUser
from bands.permissions import IsBandAdmin
from core.views import BaseAPIView, BandDependentView, TourDependentView
from core.query_params import BooleanQueryParam, ListQueryParam, QueryParam


class BaseTourView(BaseAPIView):
    def get_query_params(self) -> list[QueryParam]:
        return [BooleanQueryParam("past_dates")]


class ToursView(generics.ListCreateAPIView, BaseTourView):
    serializer_class = ToursSerializer

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return self.band_tours_response(201)

    def get_queryset(self):
        return self.get_tours_for_band()

    def get_permissions(self):
        if self.request.method == "GET":
            return (IsBandUser(),)
        return (IsBandAdmin(),)

    def get_query_params(self) -> list[QueryParam]:
        params = super().get_query_params()
        return [*params, QueryParam("include", ["all", "dates"]), BooleanQueryParam("archived_tours")]


class TourView(generics.RetrieveUpdateDestroyAPIView, BandDependentView, BaseTourView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    lookup_field = "id"
    lookup_url_kwarg = "tour_id"

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsTourUser()]
        return [IsTourAdmin()]

    def get_query_params(self) -> list[QueryParam]:
        params = super().get_query_params()
        return [*params, QueryParam("include", ["all"])]

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return self.band_response()


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
