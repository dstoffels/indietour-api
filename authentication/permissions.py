from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from authentication.models import User


class IsVerified(IsAuthenticated):
    message = {"details": "You must first verify your email address.", "code": "UNVERIFIED_EMAIL"}

    def has_permission(self, request: Request, view):
        user: User = request.user
        return super().has_permission(request, view) and user.email_verified
