from django.db import models
from core.models import UUIDModel


class Venue(UUIDModel):
    VENUE_TYPES = (
        "Amphitheater",
        "Arena",
        "Bar",
        "Brewpub",
        "Club",
        "Coffeehouse",
        "Fair",
        "Festival",
        "House",
        "Listening Room",
        "Nightclub",
        "PAC",
        "Stadium",
        "Theater",
        "Winery",
        "Other",
    )

    place = models.ForeignKey("places.Place", on_delete=models.DO_NOTHING, related_name="venues")
    creator = models.ForeignKey("authentication.User", on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    capacity = models.IntegerField()
    type = models.CharField(max_length=255, choices=[(choice, choice) for choice in VENUE_TYPES])
    last_update = models.DateTimeField(auto_now=True)
    public = models.BooleanField(default=True)

    contacts = models.ManyToManyField(to="contacts.Contact", related_name="venues")
    notes: models.QuerySet = None
    shows: models.QuerySet = None


class VenueNote(UUIDModel):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name="notes")
    user = models.OneToOneField("authentication.User", on_delete=models.CASCADE)
    note = models.TextField(default="")
