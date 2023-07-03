from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
from dates.views import DatesView

urlpatterns = [
    path("", views.ToursView.as_view(), name="tours"),
    path("/<tour_id>", views.TourView.as_view(), name="tour"),
    path("/<tour_id>/users", views.TourUsersView.as_view(), name="tourusers"),
    path("/<tour_id>/users/<touruser_id>", views.TourUserView.as_view(), name="touruser"),
    path("/<tour_id>/dates", DatesView.as_view(), name="tourdates"),
]
