from django.db import models
from core.models import UUIDModel


class Date(UUIDModel):
    tour = models.ForeignKey(
        "tours.Tour", on_delete=models.CASCADE, related_name="dates"
    )
    date = models.DateField()
    place = models.ForeignKey(
        "places.Place", on_delete=models.DO_NOTHING, null=True, related_name="dates"
    )
    title = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)

    is_show_day = models.BooleanField(default=False)

    contacts = models.ManyToManyField(to="contacts.Contact", related_name="dates")

    shows: models.QuerySet = None
    timeslots: models.QuerySet = None
    lodgings = models.QuerySet = None

    def __str__(self):
        return f"Date: {self.date}  (tour: {self.tour.name})"
