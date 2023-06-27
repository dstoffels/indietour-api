from django.db import models
from uuid_model import UUIDModel


class Date(UUIDModel):
    date = models.DateField(unique=True)
    title = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    is_show_day = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    tour = models.ForeignKey("tours.Tour", on_delete=models.CASCADE, related_name="dates")
    # place = models.ForeignKey("places.Place", on_delete=models.SET_NULL, null=True)
    # prospects = models.ManyToManyField('prospect.Prospect', related_name="dates")
    # contacts = models.ManyToManyField("contacts.DateContact", related_name='dates')

    def __str__(self):
        return f"{self.date} - {self.tour.name}"
