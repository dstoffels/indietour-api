from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from authentication.models import User
from .serializers import BandSerializer, Band, BandUserSerializer, BandUser
from authentication.permissions import IsVerified
from .permissions import IsBandUser, IsBandAdmin
from itertools import chain
from django.shortcuts import get_object_or_404


class BandsView(generics.GenericAPIView):
    queryset = Band.objects.all()
    serializer_class = BandSerializer
    permission_classes = (IsVerified,)

    def post(self, request: Request, *args, **kwargs):
        user: User = request.user
        ser = BandSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save(owner=user)
        user.active_band = ser.instance
        user.save()

        return Response(ser.data, 200)

    def get(self, request: Request, *args, **kwargs):
        user = request.user
        user_bands = list(chain(self.queryset.filter(owner=user), self.queryset.filter(banduser__user=user)))
        ser = BandSerializer(user_bands, many=True)
        return Response(ser.data, 200)


class BandView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Band.objects.all()
    serializer_class = BandSerializer
    lookup_url_kwarg = "band_id"
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsBandUser()]
        return [IsBandAdmin()]


class BandUsersView(generics.CreateAPIView):
    serializer_class = BandUserSerializer
    permission_classes = (IsBandAdmin,)
    lookup_url_kwarg = "band_id"

    def post(self, request: Request, *args, **kwargs):
        band_id = kwargs.get("band_id")
        band = get_object_or_404(Band, id=band_id)
        ser = BandUserSerializer(data=request.data, context={"band": band})
        ser.is_valid(raise_exception=True)
        ser.save()
        band_ser = BandSerializer(band)
        return Response(band_ser.data, 201)


class BandUserView(generics.RetrieveUpdateDestroyAPIView):
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
