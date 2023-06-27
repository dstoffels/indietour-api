from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from authentication.models import User
from .serializers import BandSerializer, Band, BandUserSerializer, BandUser
from authentication.permissions import IsVerified
from .permissions import IsBandUser, IsBandAdmin
from itertools import chain
from django.shortcuts import get_object_or_404


class BandsView(generics.ListCreateAPIView):
    queryset = Band.objects.all()
    serializer_class = BandSerializer
    permission_classes = (IsVerified,)

    def perform_create(self, serializer: BandSerializer):
        user: User = self.request.user
        serializer.save(owner=user)
        user.active_band = serializer.instance
        return super().perform_create(serializer)

    def get_queryset(self):
        user: User = self.request.user
        return list(chain(self.queryset.filter(owner=user), self.queryset.filter(banduser__user=user)))


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
