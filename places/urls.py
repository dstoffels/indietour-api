from django.urls import path, include
from . import views

urlpatterns = [
    path("/autocomplete", views.AutocompleteView.as_view(), name="autocomplete"),
    path("/directions", views.DirectionsView.as_view(), name="directions"),
    path("/search", views.SearchView.as_view(), name="search"),
    path("/<place_id>", views.PlaceView.as_view(), name="place"),
]
