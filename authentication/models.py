from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from .utils import generate_verification_code


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active_band = models.ForeignKey("bands.Band", on_delete=models.SET_NULL, null=True, default=None)
    active_tour = models.ForeignKey("tours.Tour", on_delete=models.SET_NULL, null=True, default=None)
    email = models.CharField(unique=True, max_length=255, null=False, editable=False)
    username = models.CharField(unique=False, max_length=255, null=False)
    email_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, default=generate_verification_code)
    member_bands = models.ManyToManyField("bands.Band", through="bands.BandUser", related_name="users")

    def get_bands(self):
        return (self.member_bands.all() | self.owned_bands.all()).order_by("name")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "password"]
