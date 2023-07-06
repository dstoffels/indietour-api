from rest_framework.request import Request
from authentication.models import User
from core.permissions import IsVerified
from .models import Contact
from core.views import BaseAPIView


class IsContactOwner(IsVerified):
    def get_permission(self):
        return super().get_permission() and self.contact.owner == self.user

    def initial(self, request: Request, view: BaseAPIView) -> None:
        super().initial(request, view)
        self.contact = Contact.objects.filter(id=self.path_vars.contact_id).first()

    def set_error_msg(self):
        self.message = {"detail": "Must be contact owner to access this resource", "code": "UNAUTHORIZED"}
