from django.db import models
from core.models import UUIDModel


class Date(UUIDModel):
    STATUS_CHOICES = ("PROSPECT", "INQUIRED", "HOLD", "CHALLENGED", "RELEASED", "OPTION", "CONFIRMED", "CANCELLED")

    tour = models.ForeignKey("tours.Tour", on_delete=models.CASCADE, related_name="dates")
    date = models.DateField()
    place = models.ForeignKey("places.Place", on_delete=models.DO_NOTHING, null=True, related_name="dates")
    title = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(
        max_length=30, default=STATUS_CHOICES[0], choices=[(choice, choice) for choice in STATUS_CHOICES]
    )
    hold = models.IntegerField(default=None, null=True)

    contacts = models.ManyToManyField(to="contacts.Contact", related_name="dates")
    # venues = models.ManyToManyField(to="venues.Venue", through="dates.Show", related_name="dates")

    shows: models.QuerySet = None
    timeslots: models.QuerySet = None
    lodgings = models.QuerySet = None

    def __str__(self):
        return f"Date: {self.date}  (tour: {self.tour.name})"


class LogEntry(UUIDModel):
    date = models.ForeignKey(Date, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    note = models.TextField(default="")
