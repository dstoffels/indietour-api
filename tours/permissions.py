from core.views import BaseAPIView
from core.views import BaseAPIView
from bands.permissions import IsBandOwner
from rest_framework.request import Request
from .models import Tour, TourUser


class IsTourUser(IsBandOwner):
    def get_permission(self):
        return super().get_permission() or bool(self.touruser)

    def set_error_msg(self):
        self.message = {"details": "Must be a tour user to access this resource.", "code": "UNAUTHORIZED"}

    def initial(self, request: Request, view: BaseAPIView):
        super().initial(request, view)
        self.tour: Tour = self.band.tours.filter(id=self.path_vars.tour_id).first()
        self.touruser: TourUser = self.tour.tourusers.filter(banduser__user=self.user).first()


class IsTourAdmin(IsTourUser):
    def get_permission(self):
        return super().get_permission() or bool(self.touruser) and self.touruser.is_admin

    def set_error_msg(self):
        self.message = {"details": "Must be a tour admin to access this resource.", "code": "REQUIRES_ADMIN"}
