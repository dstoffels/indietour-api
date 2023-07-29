from core.views import BaseAPIView
from core.views import BaseAPIView
from bands.permissions import IsBandOwner
from core.request import Request
from .models import Tour, TourUser
from django.shortcuts import get_object_or_404


class IsTourUser(IsBandOwner):
    def get_permission(self):
        return super().get_permission() or bool(self.touruser)

    def set_error_msg(self):
        self.message = {"detail": "Must be a tour user to access this resource.", "code": "UNAUTHORIZED"}

    def initial(self, request: Request, view: BaseAPIView):
        super().initial(request, view)
        self.touruser: TourUser = request.tour.tourusers.filter(banduser__user=self.user).first()


class IsTourAdmin(IsTourUser):
    def get_permission(self):
        return super().get_permission() or bool(self.touruser) and self.touruser.is_admin

    def set_error_msg(self):
        self.message = {"detail": "Must be a tour admin to access this resource.", "code": "REQUIRES_ADMIN"}
