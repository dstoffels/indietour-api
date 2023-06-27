from authentication.permissions import IsVerified
from rest_framework.request import Request
from authentication.models import User
from .models import Band
from django.shortcuts import get_object_or_404


class IsBandUser(IsVerified):
    message = {"details": "Not authorized", "code": "UNAUTHORIZED"}

    def has_permission(self, request: Request, view):
        user: User = request.user
        band_id = view.kwargs.get("band_id")
        band = get_object_or_404(Band, id=band_id)
        banduser = band.banduser_set.filter(user=user).first()

        return super().has_permission(request, view) and band.owner == user or bool(banduser)


class IsBandAdmin(IsBandUser):
    def has_permission(self, request: Request, view):
        user: User = request.user
        band_id = view.kwargs.get("band_id")
        band = get_object_or_404(Band, id=band_id)
        banduser = band.banduser_set.filter(user=user, is_admin=True).first()

        return super().has_permission(request, view) and band.owner == user or bool(banduser)
