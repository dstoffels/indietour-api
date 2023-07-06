from django.db import models
from core.models import UUIDModel


class Contact(UUIDModel):
    owner = models.ForeignKey("authentication.User", on_delete=models.CASCADE, related_name="user_contacts")
    name = models.CharField(max_length=255)
    notes = models.TextField(default="", blank=True)

    contact_methods: models.QuerySet = None
    contact_dates: models.QuerySet = None


class ContactMethod(UUIDModel):
    METHODS = ["Phone", "Email", "Facebook", "Instagram", "Whatsapp", "Twitter", "Other"]

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="contact_methods")
    method = models.CharField(max_length=255, choices=[(method, method) for method in METHODS])
    value = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.contact.name} - ${self.method}: {self.value}"

    def get_method_choices():
        return [(method, method) for method in ContactMethod.METHODS]


class ContactTitle(UUIDModel):
    title = models.CharField(max_length=255, default="")
    notes = models.TextField(default="")
