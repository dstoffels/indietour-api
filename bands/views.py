from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from authentication.models import User
from .serializers import BandSerializer, BandsSerializer, Band, BandUserSerializer, BandUser
from authentication.permissions import IsVerified
from .permissions import IsBandUser, IsBandAdmin
from django.shortcuts import get_object_or_404
from core.views import BandDependentView, BaseAPIView
from core.query_params import BooleanQueryParam, QueryParam


class BaseBandView(BaseAPIView):
    def get_query_params(self) -> list[QueryParam]:
        return [
            BooleanQueryParam("archived_tours"),
            QueryParam("include", ["tours", "dates", "all"]),
        ]


class BandsView(generics.ListCreateAPIView, BaseBandView):
    serializer_class = BandsSerializer
    permission_classes = (IsVerified,)
    # query_params = QueryParamsManager()

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return self.user_bands_response(201)

    def get_queryset(self):
        return self.get_bands_for_user()

    def get_query_params(self) -> list[QueryParam]:
        params = super().get_query_params()
        return [*params, BooleanQueryParam("archived_bands")]


class BandView(generics.RetrieveUpdateDestroyAPIView, BaseBandView):
    queryset = Band.objects.all()
    serializer_class = BandSerializer
    lookup_url_kwarg = "band_id"
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsBandUser()]
        return [IsBandAdmin()]


class BandUsersView(generics.CreateAPIView, BandDependentView, BaseBandView):
    serializer_class = BandUserSerializer
    permission_classes = (IsBandAdmin,)
    lookup_url_kwarg = "band_id"

    def finalize_response(self, request, response, *args, **kwargs):
        response = self.band_response()
        return super().finalize_response(request, response, *args, **kwargs)


class BandUserView(generics.UpdateAPIView, generics.DestroyAPIView, BandDependentView, BaseBandView):
    queryset = BandUser.objects.all()
    serializer_class = BandUserSerializer
    permission_classes = (IsBandAdmin,)
    lookup_url_kwarg = "banduser_id"
    lookup_field = "id"

    def finalize_response(self, request, response, *args, **kwargs):
        response = self.band_response()
        return super().finalize_response(request, response, *args, **kwargs)
