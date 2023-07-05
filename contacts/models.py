from django.db import models
from core.models import UUIDModel


class Contact(UUIDModel):
    owner = models.ForeignKey("authentication.User", on_delete=models.CASCADE, related_name="user_contacts")
    name = models.CharField(max_length=255)

    contact_methods = models.QuerySet = None
    places: models.QuerySet = None


class ContactMethod(UUIDModel):
    METHODS = ["Phone", "Email" "Facebook", "Instagram", "Whatsapp", "Twitter", "Other"]

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="contact_methods")
    method = models.CharField(max_length=255, choices=[(method, method) for method in METHODS])
    value = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.contact.name} - ${self.method}: {self.value}"


class PlaceDateContact(UUIDModel):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    place = models.ForeignKey("places.Place", on_delete=models.SET_NULL, null=True)
    date = models.ForeignKey("dates.Date", on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255, default="")
    notes = models.TextField(default="")
