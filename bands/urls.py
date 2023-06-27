from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path("", views.BandsView.as_view(), name="get bands"),
    path("/<band_id>", views.BandView.as_view(), name="get bands"),
    path("/<band_id>/user", views.BandUsersView.as_view(), name="add banduser"),
    path("/<band_id>/user/<banduser_id>", views.BandUserView.as_view(), name="edit banduser"),
    path("/<band_id>/tours", include("tours.urls")),
]
