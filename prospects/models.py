from django.db import models
from core.models import UUIDModel


class Prospect(UUIDModel):
    date = models.ForeignKey("dates.Date", on_delete=models.SET_NULL, null=True, related_name="prospects")
    place = models.ForeignKey("places.Place", on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True, default="")
    status = models.CharField(max_length=50)
    hold = models.IntegerField(default=0)
    log: models.QuerySet = None

    STATUS_CHOICES = ["UNCONFIRMED", "INQURY SENT", "HOLD", "UNAVAILABLE", "OFFER", "CONFIRMED"]


class LogEntry(UUIDModel):
    prospect = models.ForeignKey(Prospect, on_delete=models.CASCADE, related_name="log")
    timestamp = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True, default="")
