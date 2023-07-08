from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
from dates.views import DatesView

urlpatterns = [
    path("", views.VenueCollectionView.as_view(), name="venues"),
    path("/types", views.VenueTypesView.as_view(), name="venues"),
    path("/<venue_id>", views.VenueView.as_view(), name="venue"),
    path("/<venue_id>/notes", views.VenueNotesView.as_view(), name="venuenotes"),
    path("/<venue_id>/notes/<venuenote_id>", views.VenueNoteView.as_view(), name="venuenote"),
]
