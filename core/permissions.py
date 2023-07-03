from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from authentication.models import User
from .views import BaseAPIView


class AbstractBasePermission(IsAuthenticated):
    """Parent to the base permission class: IsVerified. Do not inherit."""

    def has_permission(self, request: Request, view: BaseAPIView):
        self.path_vars = view.path_vars
        self.initial(request, view)
        is_authenticated = super().has_permission(request, view)

        if is_authenticated:
            is_permitted = self.get_permission()
            self.set_error_msg()
            return is_permitted
        return False

    def get_permission(self):
        return True

    def set_error_msg(self):
        self.message = {"details": "Unauthorized", "code": "UNAUTHORIZED"}

    def initial(self, request: Request, view: BaseAPIView) -> None:
        """Called first in has_permissions to initialize any instance vars required for the permission."""
        self.user: User = request.user


class IsVerified(AbstractBasePermission):
    """Base Permission class for all api permissions

    Set permission criteria by overriding get_permission().

    Set error messages by overridding ser_error_msg()."""

    def get_permission(self):
        """Override to set permission criteria. super().get_permission() must be called before child criteria."""
        return self.user.email_verified

    def set_error_msg(self):
        """Override to set self.message. Called after parent permissions checked to avoid responding with wrong msg."""
        self.message = {"details": "User email not verified.", "code": "UNVERIFIED"}
