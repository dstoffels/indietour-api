from authentication.permissions import IsVerified
from rest_framework.request import Request
from authentication.models import User
from .models import Band
from django.shortcuts import get_object_or_404


class IsBandUser(IsVerified):
    def has_permission(self, request: Request, view):
        if not super().has_permission(request, view):
            return False
        self.message = {"details": "User must be added to this band.", "code": "UNAUTHORIZED"}
        user: User = request.user
        band_id = view.kwargs.get("band_id")
        band = get_object_or_404(Band, id=band_id)
        banduser = band.bandusers.filter(user=user).first()

        return band.owner == user or bool(banduser)


class IsBandAdmin(IsBandUser):
    def has_permission(self, request: Request, view):
        if not super().has_permission(request, view):
            return False
        self.message = {"details": "User must be a band admin.", "code": "REQUIRES_ADMIN"}
        user: User = request.user
        band_id = view.kwargs.get("band_id")
        band = get_object_or_404(Band, id=band_id)
        banduser = band.bandusers.filter(user=user, is_admin=True).first()

        return band.owner == user or bool(banduser)
