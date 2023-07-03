from django.db import models
from core.models import UUIDModel


class Contact(UUIDModel):
    owner = models.ForeignKey("authentication.User", on_delete=models.CASCADE, related_name="contacts")
    name = models.CharField(max_length=255)

    contact_methods = models.QuerySet = None
    places: models.QuerySet = None


class ContactMethod(UUIDModel):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="contact_methods")
    method = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
