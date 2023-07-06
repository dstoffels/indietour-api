from .models import Contact, ContactMethod
from rest_framework.exceptions import ValidationError
from bands.serializers import BandUserSerializer, serializers
from core.serializers import BaseSerializer
from core.query_params import QueryParam, ListQueryParam
from datetime import date


class ContactMethodSerializer(BaseSerializer):
    class Meta:
        model = ContactMethod
        fields = "id", "method", "value"

    method = serializers.ChoiceField(choices=ContactMethod.METHODS)
    value = serializers.CharField()

    def create(self, validated_data):
        validated_data["contact_id"] = self.path_vars.contact_id
        return super().create(validated_data)


class ContactSerializer(BaseSerializer):
    class Meta:
        model = Contact
        fields = "id", "name", "notes", "contact_methods"

    name = serializers.CharField()
    contact_methods = ContactMethodSerializer(many=True)

    def create(self, validated_data: dict):
        validated_data["owner"] = self.user

        contact_methods = validated_data.pop("contact_methods", [])
        contact = super().create(validated_data)

        for method in contact_methods:
            ContactMethod.objects.create(contact=contact, **method)

        return contact
