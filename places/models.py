from django.db import models
from core.models import UUIDModel


class Place(models.Model):
    id = models.CharField(primary_key=True, max_length=255, unique=True)
    name = models.CharField(max_length=255, blank=True)
    formatted_address = models.TextField()
    political_address = models.CharField(max_length=100)
    lat = models.DecimalField(max_digits=13, decimal_places=10, default=0)
    lng = models.DecimalField(max_digits=13, decimal_places=10, default=0)
    overview = models.TextField(default="", null=True)
    types = models.JSONField(default=list)
    business_status = models.CharField(max_length=50, default="", null=True)
    website = models.TextField(null=True)
    contacts: models.ManyToManyField(
        to="contacts.Contact", through="contacts.PlaceDateContacts", related_name="contact_places"
    )

    dates: models.QuerySet = None
    venues: models.QuerySet = None
    reviews: models.QuerySet = None

    def __str__(self) -> str:
        return self.name


class PlaceContact(UUIDModel):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="contacts")
    contact = models.ForeignKey("contacts.Contact", on_delete=models.CASCADE, related_name="contact_places")
    title = models.ForeignKey("contacts.ContactTitle", on_delete=models.CASCADE)


class PlaceReview(UUIDModel):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey("authentication.User", on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField()
    review = models.TextField()
