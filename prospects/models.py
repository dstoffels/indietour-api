from django.db import models
from core.models import UUIDModel
from django.forms.models import model_to_dict


class Prospect(UUIDModel):
    tour = models.ForeignKey("tours.Tour", on_delete=models.CASCADE, related_name="prospects")
    date = models.DateField()
    venue = models.ForeignKey("venues.Venue", on_delete=models.CASCADE)
    notes = models.TextField(blank=True, default="")
    status = models.CharField(max_length=50)
    hold = models.IntegerField(default=0)
    confirmed_date_id = models.UUIDField(unique=True, null=True)

    # models.OneToOneField(
    #     "dates.Date", on_delete=models.SET_NULL, null=True, related_name="confirmed_prospect"
    # )

    log: models.QuerySet = None

    STATUS_CHOICES = ["UNCONFIRMED", "INQURY SENT", "HOLD", "UNAVAILABLE", "OFFER", "CONFIRMED"]

    def extract_date(self):
        data = model_to_dict(self)
        data["place_id"] = self.venue.place.id
        return data


class LogEntry(UUIDModel):
    prospect = models.ForeignKey(Prospect, on_delete=models.CASCADE, related_name="log")
    timestamp = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True, default="")
