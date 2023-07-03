from django.db import models
from core.models import UUIDModel


class Lodging(UUIDModel):
    date = models.ForeignKey("dates.Date", on_delete=models.CASCADE, related_name="lodgings")
    place = models.ForeignKey("places.Place", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, default="")
    notes = models.TextField(blank=True, default="")
