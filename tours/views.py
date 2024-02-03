from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from .serializers import Tour, TourSerializer, TourUser, TourUserSerializer
from .permissions import IsTourUser, IsTourAdmin
from bands.permissions import IsBandAdmin, IsBandUser, IsBandOwner
from core.views import BaseAPIView
from core.query_params import BooleanQueryParam, ListQueryParam, QueryParam
from django.db.models import Q
from django.db.utils import IntegrityError


class BaseTourView(BaseAPIView):
    def get_query_params(self) -> list[QueryParam]:
        return [
            QueryParam("include", ["all", "dates", "prospects"]),
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
        tours = (
            Tour.objects.filter(
                Q(band_id=self.path_vars.band_id) & Q(band__owner=self.user)
                | Q(tourusers__banduser__user=self.user)
            )
            .order_by("name")
            .order_by("name")
        )
        if self.archived_tours.is_invalid():
            tours = tours.filter(is_archived=False)
        return tours

    def get_permissions(self):
        if self.request.method == "GET":
            return (IsBandUser(),)
        return (IsBandAdmin(),)


class TourView(generics.RetrieveUpdateDestroyAPIView, BaseTourView):
    model = Tour
    serializer_class = TourSerializer
    lookup_field = "id"
    lookup_url_kwarg = "tour_id"

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsTourUser()]
        return [IsTourAdmin()]


class TourUsersView(generics.CreateAPIView, BaseTourView):
    permission_classes = (IsTourAdmin,)
    serializer_class = TourUserSerializer

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return self.tour_response(201)

    def get_queryset(self):
        return TourUser.objects.filter(tour_id=self.path_vars.tour_id)


class TourUserView(generics.RetrieveUpdateDestroyAPIView, BaseTourView):
    model = TourUser
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
