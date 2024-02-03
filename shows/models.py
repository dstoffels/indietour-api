from django.db import models
from core.models import UUIDModel
from .status_choices import STATUS_CHOICES


class Show(UUIDModel):
    date = models.ForeignKey(
        "dates.Date", on_delete=models.CASCADE, related_name="shows"
    )
    venue = models.ForeignKey(
        "venues.Venue", on_delete=models.CASCADE, related_name="shows"
    )
    status = models.CharField(
        max_length=30,
        default=STATUS_CHOICES[0].get("name"),
        choices=[(choice["name"], choice["name"]) for choice in STATUS_CHOICES],
    )
    hold = models.IntegerField(default=0)
    deal = models.TextField(default="", blank=True)
    hospitality = models.TextField(default="", blank=True)
    notes = models.TextField(default="", blank=True)

    log: models.QuerySet


class LogEntry(UUIDModel):
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name="log")
    timestamp = models.DateTimeField(auto_now_add=True)
    note = models.TextField(default="")
