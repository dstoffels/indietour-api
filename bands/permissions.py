from core.permissions import IsVerified
from rest_framework.request import Request
from authentication.models import User
from .models import Band
from core.models import get_or_404
from core.views import BaseAPIView


class IsBandOwner(IsVerified):
    def get_permission(self):
        return super().get_permission() and self.band.owner == self.user

    def initial(self, request: Request, view: BaseAPIView):
        super().initial(request, view)
        self.band = Band.objects.filter(id=self.path_vars.band_id).first()


class IsBandUser(IsBandOwner):
    def get_permission(self):
        return super().get_permission() or bool(self.banduser)

    def set_error_msg(self):
        self.message = {"details": "User must be added to this band.", "code": "UNAUTHORIZED"}

    def initial(self, request: Request, view: BaseAPIView):
        super().initial(request, view)
        self.banduser = self.band.bandusers.filter(user=self.user).first()


class IsBandAdmin(IsBandUser):
    def get_permission(self):
        return super().get_permission() or bool(self.banduser) and self.banduser.is_admin

    def set_error_msg(self):
        self.message = {"details": "User must be a band admin.", "code": "REQUIRES_ADMIN"}
