from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from authentication.models import User
from .serializers import BandSerializer, Band, BandUserSerializer, BandUser
from authentication.permissions import IsVerified
from .permissions import IsBandUser, IsBandAdmin
from django.shortcuts import get_object_or_404
from core.views import BandDependentView, BaseAPIView, QueryParam


class BandsView(generics.ListCreateAPIView, BaseAPIView):
    serializer_class = BandSerializer
    permission_classes = (IsVerified,)
    query_params = [
        QueryParam("archived_tours", ["true"]),
        QueryParam("archived_bands", ["true"]),
        QueryParam("include", ["all", "tours", "dates"]),
    ]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user: User = request.user
        user.active_band_id = response.data.get("id")
        user.save()
        return self.user_bands_response(201)

    def get_queryset(self):
        return self.get_bands_for_user()


class BandView(generics.RetrieveUpdateDestroyAPIView, BaseAPIView):
    queryset = Band.objects.all()
    serializer_class = BandSerializer
    lookup_url_kwarg = "band_id"
    lookup_field = "id"
    query_params = [
        QueryParam("archived_tours", ["true"]),
        QueryParam("archived_bands", ["true"]),
        QueryParam("include", ["any", "tours", "dates"]),
    ]

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsBandUser()]
        return [IsBandAdmin()]

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return self.user_bands_response()


class BandUsersView(generics.CreateAPIView, BandDependentView):
    serializer_class = BandUserSerializer
    permission_classes = (IsBandAdmin,)
    lookup_url_kwarg = "band_id"

    def finalize_response(self, request, response, *args, **kwargs):
        response = self.band_response()
        return super().finalize_response(request, response, *args, **kwargs)


class BandUserView(generics.RetrieveUpdateDestroyAPIView, BandDependentView):
    queryset = BandUser.objects.all()
    serializer_class = BandUserSerializer
    permission_classes = (IsBandAdmin,)
    lookup_url_kwarg = "banduser_id"
    lookup_field = "id"

    def finalize_response(self, request, response, *args, **kwargs):
        response = self.band_response()
        return super().finalize_response(request, response, *args, **kwargs)
