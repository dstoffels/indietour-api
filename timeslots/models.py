from django.db import models
from core.models import UUIDModel


class Timeslot(UUIDModel):
    date = models.ForeignKey("dates.Date", on_delete=models.CASCADE, related_name="timeslots")
    description = models.TextField(default="", blank=True)
    details = models.TextField(default="", blank=True)
    start_time = models.TimeField(blank=True, null=True)
    start_after_midnight = models.BooleanField(default=False)
    end_time = models.TimeField(null=True, blank=True)
    end_after_midnight = models.BooleanField(default=False)
    origin = models.ForeignKey(
        "places.Place", on_delete=models.SET_NULL, null=True, blank=True, related_name="timeslot_origins"
    )
    destination = models.ForeignKey(
        "places.Place", on_delete=models.SET_NULL, null=True, blank=True, related_name="timeslot_destinations"
    )
    TYPES = [
        "Event",
        "Travel",
        "Flight",
        "Meeting",
    ]
    type = models.CharField(max_length=25, choices=[(choice, choice) for choice in TYPES], blank=True, default=TYPES[0])
