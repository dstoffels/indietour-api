from django.urls import path, include
from . import views

urlpatterns = [
    path("/place/details", views.PlaceView.as_view(), name="place"),
    path("/place/autocomplete", views.AutocompleteView.as_view(), name="autocomplete"),
    path("/directions", views.DirectionsView.as_view(), name="directions"),
]
