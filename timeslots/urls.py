from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.TimeslotsView.as_view(), name="timeslots"),
    path("/choices", views.TimeslotTypeChoicesView.as_view(), name="timeslot_type_choices"),
    path("/<timeslot_id>", views.TimeslotView.as_view(), name="timeslot"),
]
