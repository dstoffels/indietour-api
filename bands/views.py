from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from authentication.models import User
from .serializers import BandSerializer, Band, BandUserSerializer, BandUser
from authentication.permissions import IsVerified
from .permissions import IsBandUser, IsBandAdmin
from itertools import chain
from django.shortcuts import get_object_or_404
from core.views import BaseAPIView


class BandsView(generics.ListCreateAPIView, BaseAPIView):
    queryset = Band.objects.all()
    serializer_class = BandSerializer
    permission_classes = (IsVerified,)

    def get_queryset(self):
        user: User = self.request.user
        return list(chain(self.queryset.filter(owner=user), self.queryset.filter(banduser__user=user)))


class BandView(generics.RetrieveUpdateDestroyAPIView, BaseAPIView):
    queryset = Band.objects.all()
    serializer_class = BandSerializer
    lookup_url_kwarg = "band_id"
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsBandUser()]
        return [IsBandAdmin()]


class BandUsersView(generics.CreateAPIView, BaseAPIView):
    serializer_class = BandUserSerializer
    permission_classes = (IsBandAdmin,)
    lookup_url_kwarg = "band_id"

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        band = get_object_or_404(Band, id=kwargs.get("band_id"))
        return Response(BandSerializer(band).data, 201)


class BandUserView(generics.RetrieveUpdateDestroyAPIView, BaseAPIView):
    queryset = BandUser.objects.all()
    serializer_class = BandUserSerializer
    permission_classes = (IsBandAdmin,)
    lookup_url_kwarg = "banduser_id"
    lookup_field = "id"

    def patch(self, request, *args, **kwargs):
        band = self.get_object().band
        super().patch(request, *args, **kwargs)
        return Response(BandSerializer(band).data, 200)

    def delete(self, request, *args, **kwargs):
        band = self.get_object().band
        super().delete(request, *args, **kwargs)
        return Response(BandSerializer(band).data, 204)
