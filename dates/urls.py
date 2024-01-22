from django.urls import path, include
from . import views
from shows.views import ShowsView
from timeslots.views import TimeslotsView
from lodgings.views import LodgingsView

urlpatterns = [
    path("/<date_id>", views.DateView.as_view()),
    path("/<date_id>/logentries", views.DateLogView.as_view()),
    path("/<date_id>/logentries/<logentry_id>", views.LogEntryView.as_view()),
    path("/<date_id>/contacts/<contact_id>", views.DateContactView.as_view()),
    path("/<date_id>/shows", ShowsView.as_view()),
    path("/<date_id>/timeslots", TimeslotsView.as_view()),
    path("/<date_id>/lodgings", LodgingsView.as_view()),
]
