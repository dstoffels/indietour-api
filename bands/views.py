from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from core.query_params import QueryParam
from authentication.models import User
from .serializers import BandSerializer, BandsSerializer, Band, BandUserSerializer, BandUser
from authentication.permissions import IsVerified
from .permissions import IsBandUser, IsBandAdmin
from django.shortcuts import get_object_or_404
from core.views import BandDependentView, BaseAPIView
from core.query_params import BooleanQueryParam, QueryParam, QueryParamsManager


class BandsView(generics.ListCreateAPIView, BaseAPIView):
    serializer_class = BandsSerializer
    permission_classes = (IsVerified,)
    # query_params = QueryParamsManager()

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return self.user_bands_response(201)

    def get_queryset(self):
        return self.get_bands_for_user()

    def init_query_params(self) -> list[QueryParam]:
        return [
            BooleanQueryParam("archived_tours"),
            BooleanQueryParam("archived_bands"),
            QueryParam("include", ["tours", "dates"]),
        ]


class BandView(generics.RetrieveUpdateDestroyAPIView, BaseAPIView):
    queryset = Band.objects.all()
    serializer_class = BandSerializer
    lookup_url_kwarg = "band_id"
    lookup_field = "id"
    # query_params = QueryParamsManager(
    #     BooleanQueryParam("archived_tours"),
    #     QueryParam("include", ["tours", "dates"]),
    # )

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsBandUser()]
        return [IsBandAdmin()]


class BandUsersView(generics.CreateAPIView, BandDependentView):
    serializer_class = BandUserSerializer
    permission_classes = (IsBandAdmin,)
    lookup_url_kwarg = "band_id"

    def finalize_response(self, request, response, *args, **kwargs):
        response = self.band_response()
        return super().finalize_response(request, response, *args, **kwargs)


class BandUserView(generics.DestroyAPIView, BandDependentView):
    queryset = BandUser.objects.all()
    serializer_class = BandUserSerializer
    permission_classes = (IsBandAdmin,)
    lookup_url_kwarg = "banduser_id"
    lookup_field = "id"

    def finalize_response(self, request, response, *args, **kwargs):
        response = self.band_response()
        return super().finalize_response(request, response, *args, **kwargs)
