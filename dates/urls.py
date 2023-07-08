from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.DatesView.as_view(), name="tourdates"),
    path("/<date_id>", views.DateView.as_view(), name="date"),
    path("/<date_id>/logentries", views.DateLogView.as_view(), name="logentries"),
    path("/<date_id>/logentries/<logentry_id>", views.LogEntryView.as_view(), name="logentry"),
    path("/<date_id>/contacts/<contact_id>", views.DateContactView.as_view(), name="datecontact"),
    path("/<date_id>/shows", include("shows.urls")),
    path("/<date_id>/timeslots", include("timeslots.urls")),
    path("/<date_id>/lodgings", include("lodgings.urls")),
]
