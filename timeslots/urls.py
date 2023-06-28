from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.TimeslotsView.as_view(), name="timeslots"),
    path("/<timeslot_id>", views.TimeslotView.as_view(), name="timeslot"),
]
