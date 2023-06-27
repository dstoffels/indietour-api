from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path("", views.BandsView.as_view(), name="get bands"),
    path("/<band_id>", views.BandGetter.as_view(), name="get bands"),
    path("/<band_id>/user", views.BandUserView.as_view(), name="add band user"),
]
