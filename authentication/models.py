from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from .utils import generate_verification_code
from rest_framework.request import Request
from django.contrib.auth import authenticate
from datetime import datetime


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active_band_id = models.UUIDField(null=True, default=None)
    active_tour_id = models.UUIDField(null=True, default=None)
    email = models.CharField(unique=True, max_length=255, null=False, editable=False)
    username = models.CharField(unique=True, max_length=255, null=False)
    email_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, default=generate_verification_code)
    last_login = models.DateTimeField(auto_now=True)

    member_bands = models.ManyToManyField("bands.Band", through="bands.BandUser", related_name="users")
    owned_bands = models.QuerySet
    contacts: models.QuerySet = None

    def get_bands(self):
        return (self.member_bands.all() | self.owned_bands.all()).order_by("name")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "password"]

    def login(request: Request):
        email = request.data.get("email")
        password = request.data.get("password")

        user: User = authenticate(request, email=email, password=password)
        user.last_login = datetime.now()
        user.save()

        return user
