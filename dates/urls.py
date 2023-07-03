from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.DatesView.as_view(), name="tourdates"),
    path("/<date_id>", views.DateView.as_view(), name="date"),
    path("/<date_id>/timeslots", include("timeslots.urls")),
    path("/<date_id>/prospects", include("prospects.urls")),
    path("/<date_id>/lodgings", include("lodgings.urls")),
]
