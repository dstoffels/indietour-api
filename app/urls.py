from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin", admin.site.urls),
    path("auth", include("authentication.urls")),
    path("bands", include("bands.urls")),
    path("places", include("places.urls")),
    path("venues", include("venues.urls")),
    path("contacts", include("contacts.urls")),
]
