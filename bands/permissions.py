from core.permissions import IsVerified
from core.request import Request
from authentication.models import User
from .models import Band, BandUser
from core.views import BaseAPIView


class IsBandOwner(IsVerified):
    def get_permission(self):
        return super().get_permission() and self.band.owner == self.user

    def initial(self, request: Request, view: BaseAPIView):
        super().initial(request, view)
        self.band = request.band

    def set_error_msg(self):
        self.message = {"details": "Must be the band owner to access this resource.", "code": "UNAUTHORIZED"}


class IsBandUser(IsBandOwner):
    def get_permission(self):
        return super().get_permission() or bool(self.banduser)

    def set_error_msg(self):
        self.message = {"details": "Must be a band member to access this resource.", "code": "UNAUTHORIZED"}

    def initial(self, request: Request, view: BaseAPIView):
        super().initial(request, view)
        self.banduser: BandUser = self.band.bandusers.filter(user=self.user).first()
        print(self.banduser)


class IsBandAdmin(IsBandUser):
    def get_permission(self):
        if self.banduser:
            return super().get_permission() and self.banduser.is_admin
        return super().get_permission()

    def set_error_msg(self):
        self.message = {"details": "Must be a band admin to access this resource.", "code": "REQUIRES_ADMIN"}
