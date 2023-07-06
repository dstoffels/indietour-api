from rest_framework import generics
from rest_framework.request import Request
from .serializers import Contact, ContactSerializer, ContactMethod, ContactMethodSerializer
from .permissions import IsVerified, IsContactOwner
from core.views import BaseAPIView
from core.query_params import ListQueryParam, BooleanQueryParam, QueryParam
from datetime import date


class ContactsView(generics.ListCreateAPIView, BaseAPIView):
    serializer_class = ContactSerializer
    permission_classes = (IsVerified,)

    def get_queryset(self):
        return Contact.objects.filter(owner=self.user)


class ContactView(generics.RetrieveUpdateDestroyAPIView, BaseAPIView):
    serializer_class = ContactSerializer
    permission_classes = (IsVerified,)
    lookup_field = "id"
    lookup_url_kwarg = "contact_id"

    def get_queryset(self):
        return Contact.objects.filter(owner=self.user)

    def get_permissions(self):
        if self.request.method != "GET":
            return (IsContactOwner(),)
        return super().get_permissions()


class ContactMethodsView(generics.ListCreateAPIView, BaseAPIView):
    serializer_class = ContactMethodSerializer
    permission_classes = (IsContactOwner,)

    def get_queryset(self):
        return ContactMethod.objects.filter(contact_id=self.path_vars.contact_id)


class ContactMethodView(generics.RetrieveUpdateDestroyAPIView, BaseAPIView):
    serializer_class = ContactMethodSerializer
    permission_classes = (IsContactOwner,)
    lookup_field = "id"
    lookup_url_kwarg = "contactmethod_id"

    def get_queryset(self):
        return ContactMethod.objects.filter(contact_id=self.path_vars.contact_id)
