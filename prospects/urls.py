from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.ProspectsView.as_view(), name="prospects"),
    path("/<prospect_id>", views.ProspectView.as_view(), name="prospect"),
    # path("/<prospect_id>/log", views.DateView.as_view(), name="date"),
    # path("/<prospect_id>/log/<logentry_id>", views.DateView.as_view(), name="date"),
]
