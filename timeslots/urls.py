from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.TimeslotsView.as_view(), name="timeslots"),
]
