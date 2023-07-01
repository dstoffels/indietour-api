from django.db import models
from core.models import UUIDModel


class Tour(UUIDModel):
    name = models.CharField(max_length=255, error_messages={"unique": "Name must be unique."})
    band = models.ForeignKey("bands.Band", on_delete=models.CASCADE, related_name="tours")
    users = models.ManyToManyField(to="TourUser", related_name="users_tours")
    is_archived = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Tour: {self.name} (band: {self.band.name})"


class TourUser(UUIDModel):
    banduser = models.ForeignKey("bands.BandUser", on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="tourusers")

    def __str__(self) -> str:
        return f"{self.banduser.user.email} ({self.tour.name})"
