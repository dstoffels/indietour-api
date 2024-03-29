from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from authentication.models import User
from .serializers import (
    BandSerializer,
    BandsSerializer,
    Band,
    BandUserSerializer,
    BandUser,
)
from core.permissions import IsVerified
from .permissions import IsBandUser, IsBandAdmin, IsBandOwner
from django.shortcuts import get_object_or_404
from core.views import BaseAPIView
from core.query_params import BooleanQueryParam, QueryParam
from django.db.models import Q
from django.db.utils import IntegrityError


class BaseBandView(BaseAPIView):
    def get_query_params(self) -> list[QueryParam]:
        return [
            BooleanQueryParam("archived_tours"),
            BooleanQueryParam("past_dates"),
            QueryParam("include", ["tours", "dates", "all"]),
        ]


class BandsView(generics.ListCreateAPIView, BaseBandView):
    serializer_class = BandsSerializer
    permission_classes = (IsVerified,)

    def get_queryset(self):
        user: User = self.request.user
        bands = user.get_bands()
        if self.archived_bands.is_invalid():
            bands = bands.filter(is_archived=False)

        return bands

    def get_query_params(self) -> list[QueryParam]:
        params = super().get_query_params()
        return [*params, BooleanQueryParam("archived_bands")]

    def init_query_params(self, request: Request):
        self.archived_bands: QueryParam
        self.archived_tours: QueryParam
        self.include: QueryParam
        super().init_query_params(request)

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except IntegrityError as e:
            return Response({"detail": "Cannot have duplicate bands."}, 400)


class BandView(generics.RetrieveUpdateDestroyAPIView, BaseBandView):
    model = Band
    serializer_class = BandSerializer
    lookup_url_kwarg = "band_id"
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method == "GET":
            return (IsBandUser(),)
        if self.request.method == "DELETE":
            return (IsBandOwner(),)
        return (IsBandAdmin(),)


class BandUsersView(generics.CreateAPIView, BaseBandView):
    serializer_class = BandUserSerializer
    permission_classes = (IsBandAdmin,)
    lookup_url_kwarg = "band_id"

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return self.band_response()


class BandUserView(generics.UpdateAPIView, generics.DestroyAPIView, BaseBandView):
    model = BandUser
    serializer_class = BandUserSerializer
    permission_classes = (IsBandAdmin,)
    lookup_url_kwarg = "banduser_id"
    lookup_field = "id"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return self.band_response()
