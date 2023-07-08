from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.ShowsView.as_view(), name="shows"),
    path("/<show_id>", views.ShowView.as_view(), name="show"),
]
