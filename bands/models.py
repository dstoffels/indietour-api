from django.db import models
from core.models import UUIDModel
from django.contrib import admin


class Band(UUIDModel):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(
        "authentication.User", on_delete=models.CASCADE, related_name="owned_bands"
    )
    is_archived = models.BooleanField(default=False)
    tours: models.QuerySet = None
    bandusers: models.QuerySet = None

    class Meta:
        unique_together = "name", "owner"

    def __str__(self) -> str:
        return f"Band: {self.name}"


class BandUser(UUIDModel):
    band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name="bandusers")
    user = models.ForeignKey("authentication.User", on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.user.email} ({self.band})"


# ADMIN
class BandUserInline(admin.TabularInline):
    model = BandUser
    extra = 1


class BandAdmin(admin.ModelAdmin):
    inlines = [BandUserInline]
