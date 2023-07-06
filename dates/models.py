from django.db import models
from core.models import UUIDModel


class Date(UUIDModel):
    date = models.DateField()
    title = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    is_show_day = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    tour = models.ForeignKey("tours.Tour", on_delete=models.CASCADE, related_name="dates")
    place = models.ForeignKey("places.Place", on_delete=models.DO_NOTHING, null=True, related_name="dates")

    contacts: models.ManyToManyField(to="contacts.Contact", through="dates.DateContact", related_name="contact_dates")
    timeslots: models.QuerySet = None
    prospects: models.QuerySet = None
    lodgings = models.QuerySet = None

    def __str__(self):
        return f"Date: {self.date}  (tour: {self.tour.name})"


class DateContact(UUIDModel):
    date = models.ForeignKey(Date, on_delete=models.CASCADE, related_name="contacts")
    contact = models.ForeignKey("contacts.Contact", on_delete=models.CASCADE, related_name="contact_dates")
    title = models.CharField(max_length=255)
