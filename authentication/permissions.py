from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from authentication.models import User


class IsVerified(IsAuthenticated):
    def has_permission(self, request: Request, view):
        if not super().has_permission(request, view):
            return False
        self.message = {"details": "User must verify their email.", "code": "UNVERIFIED"}
        user: User = request.user
        return user.email_verified
