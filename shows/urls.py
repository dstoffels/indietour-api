from django.urls import path, include
from . import views

urlpatterns = [
    path("/statuses", views.ShowStatusView.as_view()),
    path("", views.ShowsView.as_view()),
    path("/<show_id>", views.ShowView.as_view()),
]
