from rest_framework import serializers
from .models import Date, DateContact
from contacts.serializers import ContactSerializer
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from timeslots.serializers import TimeslotSerializer
from lodgings.serializers import LodgingSerializer
from places.serializers import PlaceSerializer, Place
from core.serializers import BaseSerializer
from core.query_params import BooleanQueryParam, ListQueryParam


class DateContactSerializer(BaseSerializer):
    class Meta:
        model = DateContact
        fields = "id", "contact", "title", "notes", "contact_id"

    contact = ContactSerializer(read_only=True)
    contact_id = serializers.UUIDField(write_only=True)

    title = serializers.SerializerMethodField()
    notes = serializers.SerializerMethodField()

    def get_title(self, datecontact: DateContact):
        return datecontact.title.title

    def get_notes(self, datecontact: DateContact):
        return datecontact.title.notes

    def create(self, validated_data):
        validated_data["date_id"] = self.path_vars.date_id
        print(self.initial_data)

        return super().create(validated_data)


class DateSerializer(BaseSerializer):
    class Meta:
        model = Date
        fields = (
            "id",
            "date",
            "title",
            "place",
            "place_id",
            "notes",
            "is_show_day",
            "is_confirmed",
            "timeslots",
            "lodgings",
            "contacts",
        )

    place = PlaceSerializer(read_only=True)
    place_id = serializers.CharField(write_only=True)
    timeslots = TimeslotSerializer(read_only=True, many=True)
    lodgings = LodgingSerializer(read_only=True, many=True)
    contacts = DateContactSerializer(read_only=True, many=True)

    def create(self, validated_data: dict):
        tour_id = self.path_vars.tour_id
        validated_data["tour_id"] = tour_id
        duplicate = Date.objects.filter(tour_id=tour_id, date=validated_data.get("date")).first()
        if duplicate:
            raise ValidationError({"details": "Cannot have duplicate dates in a tour.", "code": "DUPLICATE"})

        ser = PlaceSerializer(data=validated_data, context=self.context)
        ser.is_valid()
        ser.save()

        return super().create(validated_data)

    def update(self, instance, validated_data):
        ser = PlaceSerializer(data=validated_data)
        ser.is_valid()
        ser.save()
        return super().update(instance, validated_data)

    def init_query_params(self):
        self.include: ListQueryParam
        self.past_dates: BooleanQueryParam

    def get_fields(self):
        fields = super().get_fields()
        if not self.include.contains("all"):
            if not self.include.contains("timeslots"):
                fields.pop("timeslots")
            if not self.include.contains("lodgings"):
                fields.pop("lodgings")

        return fields
