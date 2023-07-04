from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
from dates.views import DatesView

urlpatterns = [
    path("", views.VenueCollectionView.as_view(), name="venues"),
    path("/<venue_id>", views.VenueView.as_view(), name="venues"),
]
