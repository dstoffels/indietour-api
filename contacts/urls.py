from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path("", views.ContactsView.as_view(), name="contacts"),
    path("/<contact_id>", views.ContactView.as_view(), name="contact"),
    path("/<contact_id>/methods", views.ContactMethodsView.as_view(), name="contact"),
    path("/<contact_id>/methods/<contactmethod_id>", views.ContactMethodView.as_view(), name="contact"),
]
