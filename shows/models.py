from django.db import models
from core.models import UUIDModel


class Show(UUIDModel):
    date = models.ForeignKey("dates.Date", on_delete=models.CASCADE, related_name="shows")
    venue = models.ForeignKey("venues.Venue", on_delete=models.CASCADE)
    deal = models.TextField(default="", blank=True)
    hospitality = models.TextField(default="", blank=True)
    notes = models.TextField(default="", blank=True)
