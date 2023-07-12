from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("api/admin", admin.site.urls),
    path("api/auth", include("authentication.urls")),
    path("api/bands", include("bands.urls")),
    path("api/places", include("places.urls")),
    path("api/venues", include("venues.urls")),
    path("api/contacts", include("contacts.urls")),
]
