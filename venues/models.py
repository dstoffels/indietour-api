from django.db import models
from core.models import UUIDModel


class Venue(UUIDModel):
    place = models.ForeignKey("places.Place", on_delete=models.DO_NOTHING, related_name="venues")
    creator = models.ForeignKey("authentication.User", on_delete=models.SET_NULL, null=True)
    is_public = models.BooleanField(default=False)
    capacity = models.IntegerField()
    type = models.CharField(max_length=255)

    notes: models.QuerySet = None


class VenueNote(UUIDModel):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name="notes")
    user = models.OneToOneField("authentication.User", on_delete=models.CASCADE)
    note = models.TextField(default="")
