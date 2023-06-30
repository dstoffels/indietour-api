from rest_framework import generics
from rest_framework.exceptions import ValidationError
from bands.serializers import Band, BandSerializer
from tours.serializers import Tour, TourSerializer
from dates.serializers import Date, DateSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.request import Request
from django.db.models import Q


class QueryParam:
    def __init__(self, name: str, accepted_values=[]):
        self.name = name
        self.accepted_values = accepted_values
        self.value = ""

    def validate(self, value: str):
        self.value = value
        is_valid = (
            self.value is None or self.value.lower() in self.accepted_values if len(self.accepted_values) else True
        )
        self.value = self.value == "true" if self.value == "true" else value
        return is_valid

    def __repr__(self) -> str:
        return self.name


class BaseAPIView(generics.GenericAPIView):
    """Base for all indietour views.

    Path variables are automatically assigned to serializer context."""

    query_params: list[QueryParam] = []
    validated_query_params: dict[str, str] = {}
    """Add QueryParams expected for this view"""

    def validate_query_params(self):
        invalid_params: list[QueryParam] = []
        for param in self.query_params:
            value = self.request.query_params.get(param.name)
            if not param.validate(value):
                invalid_params.append(param)
        if len(invalid_params):
            raise ValidationError(
                {
                    "details": "Invalid query parameter value(s)",
                    "invalid_params": [
                        {param.name: param.value, "accepted values": param.accepted_values} for param in invalid_params
                    ],
                }
            )
        self.validated_query_params = {param.name: param.value for param in self.query_params}

    def get_serializer_context(self):
        """Adds path variables and query params to serializer context dict. Query params are validated before being added."""
        context = super().get_serializer_context()
        context.update(self.kwargs)

        self.validate_query_params()
        context.update(self.validated_query_params)

        return context

    def get_bands_for_user(self):
        user = self.request.user
        bands = Band.objects.filter(Q(owner=user) | Q(banduser__user=user)).order_by("name")
        return bands

    def user_bands_response(self, status_code=200):
        bands = self.get_bands_for_user()
        ser = BandSerializer(bands, many=True, context=self.get_serializer_context())
        return Response(ser.data, status_code)

    def band_response(self, status_code=200):
        band = get_object_or_404(Band, id=self.kwargs.get("band_id"))
        ser = BandSerializer(band, context=self.get_serializer_context())
        return Response(ser.data, status_code)

    def tour_response(self, status_code=200):
        tour = get_object_or_404(Tour, id=self.kwargs.get("tour_id"))
        ser = TourSerializer(tour, context=self.get_serializer_context())
        return Response(ser.data, status_code)


class BandDependentView(BaseAPIView):
    def initial(self, request, *args, **kwargs):
        try:
            obj = self.get_object()
            self.validate_band(obj, **kwargs)
        except:
            pass
        return super().initial(request, *args, **kwargs)

    def validate_band(self, band_dependent_obj, **kwargs):
        band_id = kwargs.get("band_id")
        try:
            if str(band_dependent_obj.band.id) != band_id:
                raise ValidationError(
                    {
                        "details": f"{band_dependent_obj} does not belong to the provided band. band_id: {band_id}",
                        "code": "invalid",
                    }
                )
        except:
            raise ValidationError


class TourDependentView(BandDependentView):
    def initial(self, request, *args, **kwargs):
        if request.method == "POST":
            tour_id = kwargs.get("tour_id")
            tour = Tour.objects.filter(id=tour_id).first()
            self.validate_band(tour, **kwargs)
        else:
            obj = self.get_object()
            self.validate_tour(obj, **kwargs)
            self.validate_band(obj.tour, **kwargs)

        return super().initial(request, *args, **kwargs)

    def validate_tour(self, tour_dependent_obj, **kwargs):
        tour_id = kwargs.get("tour_id")
        try:
            if str(tour_dependent_obj.tour.id) != tour_id:
                raise ValidationError(
                    {
                        "details": f"{tour_dependent_obj} does not belong to the provided tour. tour_id {tour_id}",
                        "code": "invalid",
                    }
                )
        except:
            raise ValidationError


class DateDependentView(TourDependentView):
    def initial(self, request, *args, **kwargs):
        try:
            obj = self.get_object()
            self.validated_date(obj, **kwargs)
            self.validate_tour(obj.date, **kwargs)
            self.validate_band(obj.date.tour, **kwargs)
        except:
            date_id = kwargs.get("date_id")
            date = Date.objects.only("tour_id").filter(id=date_id).first()
            self.validate_tour(date, **kwargs)
        return super().initial(request, *args, **kwargs)

    def validated_date(self, date_dependent_obj, **kwargs):
        date_id = kwargs.get("date_id")
        try:
            if str(date_dependent_obj.date.id) != date_id:
                raise ValidationError(
                    {
                        "details": f"{date_dependent_obj} does not belong to the provided date. date_id: {date_id}",
                        "code": "invalid",
                    }
                )
        except:
            raise ValidationError
