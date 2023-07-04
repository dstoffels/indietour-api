from django.db import models
from core.models import UUIDModel


class Venue(UUIDModel):
    place = models.ForeignKey("places.Place", on_delete=models.DO_NOTHING)
    capacity = models.IntegerField()
    type = models.CharField(max_length=255)
