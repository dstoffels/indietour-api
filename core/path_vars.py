from bands.models import Band
from tours.models import Tour
from dates.models import Date
from rest_framework.exceptions import ValidationError
from django.db import models


class PathVars:
    def __init__(self, kwargs: dict) -> None:
        self.band_id = kwargs.get("band_id")
        self.banduser_id = kwargs.get("banduser_id")
        self.tour_id = kwargs.get("tour_id")
        self.touruser_id = kwargs.get("touruser_id")
        self.date_id = kwargs.get("date_id")
        self.place_id = kwargs.get("place_id")
        self.show_id = kwargs.get("show_id")
        self.placecontact_id = kwargs.get("placecontact_id")
        self.timeslot_id = kwargs.get("timeslot_id")
        self.lodging_id = kwargs.get("lodging_id")
        self.contact_id = kwargs.get("contact_id")
        self.contactmethod_id = kwargs.get("contact_id")
        self.datecontact_id = kwargs.get("contact_id")
        self.placecontact_id = kwargs.get("contact_id")
        self.venue_id = kwargs.get("venue_id")
        self.venuenote_id = kwargs.get("venuenote_id")
        self.validate()

    def update_context(self, context: dict):
        context.update({"path_vars": self})

    def to_obj_attrs(self, obj):
        for key, value in vars(self).items():
            setattr(obj, key, value)

    def validate(self):
        """Validates all input path variable ids to ensure integrity between related models"""
        if self.band_id:
            band: Band = Band.objects.filter(id=self.band_id).first()
            self._validate_id(band.bandusers, self.banduser_id, "band")
            tour: Tour = self._validate_id(band.tours, self.tour_id, "band")
            if tour:
                self._validate_id(tour.tourusers, self.touruser_id, "tour")
                date: Date = self._validate_id(tour.dates, self.date_id, "tour")
                if date:
                    self._validate_id(date.timeslots, self.timeslot_id, "date")
                    self._validate_id(date.lodgings, self.lodging_id, "date")

    def _validate_id(self, queryset: models.QuerySet, id, model_name: str):
        if id:
            obj: models.Model = queryset.filter(id=id).first()
            if obj:
                return obj
            raise ValidationError(
                {
                    "details": f"id: {id} does not belong to the provided path variable: {model_name.lower()}_id.",
                    "code": "invalid",
                }
            )
