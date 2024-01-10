from django.db import models
from core.models import UUIDModel


class Timeslot(UUIDModel):
    date = models.ForeignKey("dates.Date", on_delete=models.CASCADE, related_name="timeslots")
    title = models.CharField(max_length=255, default="", blank=True)
    type = models.CharField(max_length=25)
    details = models.TextField(default="", blank=True)
    start_time = models.TimeField(blank=True, null=True)
    origin = models.ForeignKey(
        "places.Place", on_delete=models.DO_NOTHING, null=True, blank=True, related_name="timeslot_origins"
    )
    start_after_midnight = models.BooleanField(default=False)
    end_time = models.TimeField(null=True, blank=True)
    destination = models.ForeignKey(
        "places.Place", on_delete=models.DO_NOTHING, null=True, blank=True, related_name="timeslot_destinations"
    )
    end_after_midnight = models.BooleanField(default=False)

    TYPES = ["Event", "Travel", "Flight", "Meeting"]
