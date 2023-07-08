from core.views import BaseAPIView
from core.views import BaseAPIView
from core.permissions import IsVerified
from rest_framework.request import Request
from .models import Venue, VenueNote


class IsVenueOwner(IsVerified):
    def get_permission(self):
        if self.venue:
            return super().get_permission() and self.venue.creator == self.user

    def set_error_msg(self):
        self.message = {"detail": "Must be venue owner to access this resource", "code": "UNAUTHORIZED"}

    def initial(self, request: Request, view: BaseAPIView) -> None:
        super().initial(request, view)
        self.venue = Venue.objects.filter(id=self.path_vars.venue_id).first()


class IsPublicVenue(IsVenueOwner):
    def get_permission(self):
        if self.venue:
            return super().get_permission() or self.venue.is_public

    def set_error_msg(self):
        self.message = {"detail": "This venue is not public.", "code": "UNAUTHORIZED"}


class IsNoteOwner(IsVerified):
    def get_permission(self):
        return super().get_permission() and self.venuenote.user == self.user

    def set_error_msg(self):
        self.message = {"detail": "Must be owner of this note to access this resource", "code": "UNAUTHORIZED"}

    def initial(self, request: Request, view: BaseAPIView) -> None:
        super().initial(request, view)
        self.venuenote = VenueNote.objects.filter(id=self.path_vars.venuenote_id).first()
