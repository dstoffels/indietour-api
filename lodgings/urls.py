from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.LodgingsView.as_view(), name="lodgings"),
    path("/<lodging_id>", views.LodgingView.as_view(), name="lodging"),
]
