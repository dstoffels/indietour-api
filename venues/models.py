from django.db import models
from core.models import UUIDModel


class Venue(UUIDModel):
    place = models.ForeignKey("places.Place", on_delete=models.DO_NOTHING)
    creator = models.ForeignKey("authentication.User", on_delete=models.SET_NULL, null=True)
    is_public = models.BooleanField(default=False)
    capacity = models.IntegerField()
    type = models.CharField(max_length=255)


class VenueNote(UUIDModel):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    user = models.ForeignKey("authentication.User", on_delete=models.CASCADE, unique=True)
    note = models.TextField(default="")
