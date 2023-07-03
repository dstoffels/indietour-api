from django.db import models


class Place(models.Model):
    id = models.CharField(primary_key=True, max_length=255, unique=True)
    name = models.CharField(max_length=255, blank=True)
    formatted_address = models.TextField()
    political_address = models.CharField(max_length=100)
    lat = models.DecimalField(max_digits=13, decimal_places=10, default=0)
    lng = models.DecimalField(max_digits=13, decimal_places=10, default=0)
    dates: models.QuerySet
    # contacts = models.ManyToManyField("contacts.Contact", through="contacts.PlaceContact" related_name="places", blank=True)

    def __str__(self) -> str:
        return self.description
