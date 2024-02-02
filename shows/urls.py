from django.urls import path, include
from . import views

urlpatterns = [
    path("/statuses", views.ShowStatusView.as_view()),
    path("", views.ShowsView.as_view()),
    path("/<show_id>", views.ShowView.as_view()),
    path("/<show_id>/logentries", views.DateLogView.as_view()),
    path("/<show_id>/logentries/<logentry_id>", views.LogEntryView.as_view()),
]
