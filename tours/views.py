from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from .serializers import Tour, TourSerializer, TourUser, TourUserSerializer
from .permissions import IsTourUser, IsTourAdmin
from bands.permissions import IsBandAdmin, IsBandUser, IsBandOwner
from core.views import BaseAPIView
from core.query_params import BooleanQueryParam, ListQueryParam, QueryParam


class BaseTourView(BaseAPIView):
    def get_query_params(self) -> list[QueryParam]:
        return [
            QueryParam("include", ["all", "dates"]),
            BooleanQueryParam("past_dates"),
            BooleanQueryParam("archived_tours"),
        ]

    def init_query_params(self, request: Request):
        super().init_query_params(request)
        self.include: QueryParam
        self.past_dates: QueryParam
        self.archived_tours: QueryParam


class ToursView(generics.ListCreateAPIView, BaseTourView):
    serializer_class = TourSerializer

    def get_queryset(self):
        tours = Tour.objects.filter(band_id=self.kwargs.get("band_id")).order_by("name")
        if self.archived_tours.is_invalid():
            tours = tours.filter(is_archived=False)
        return tours

    def get_permissions(self):
        if self.request.method == "GET":
            return (IsBandUser(),)
        return (IsBandAdmin(),)


class TourView(generics.RetrieveUpdateDestroyAPIView, BaseTourView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    lookup_field = "id"
    lookup_url_kwarg = "tour_id"

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsTourUser()]
        return [IsTourAdmin()]


class TourUsersView(generics.CreateAPIView, BaseTourView):
    queryset = TourUser.objects.all()
    permission_classes = (IsTourAdmin,)
    serializer_class = TourUserSerializer

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return self.tour_response(201)


class TourUserView(generics.RetrieveUpdateDestroyAPIView, BaseTourView):
    queryset = TourUser.objects.all()
    permission_classes = (IsTourAdmin,)
    serializer_class = TourUserSerializer
    lookup_url_kwarg = "touruser_id"
    lookup_field = "id"

    def patch(self, request, *args, **kwargs):
        super().patch(request, *args, **kwargs)
        return self.tour_response()

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return self.tour_response()
