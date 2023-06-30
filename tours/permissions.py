from bands.permissions import IsBandUser, IsBandAdmin
from rest_framework.request import Request
from authentication.models import User
from .models import Tour
from django.shortcuts import get_object_or_404


class IsTourUser(IsBandUser):
    def has_permission(self, request: Request, view):
        if not super().has_permission(request, view):
            return False
        self.message = {"details": "User must be added to this tour.", "code": "UNAUTHORIZED"}
        user: User = request.user
        tour_id = view.kwargs.get("tour_id")
        tour = get_object_or_404(Tour, id=tour_id)
        touruser = tour.tourusers.filter(banduser__user=user).first()

        return tour.band.owner == user or bool(touruser)


class IsTourAdmin(IsBandUser):
    def has_permission(self, request: Request, view):
        if not super().has_permission(request, view):
            return False
        self.message = {"details": "User must be a band admin", "code": "REQUIRES_ADMIN"}
        user: User = request.user
        tour_id = view.kwargs.get("tour_id")
        tour = get_object_or_404(Tour, id=tour_id)
        touruser = tour.tourusers.filter(banduser__user=user, banduser__is_admin=True).first()

        return tour.band.owner == user or bool(touruser)
