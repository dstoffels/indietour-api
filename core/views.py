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
    def __init__(self, name: str, accepted_values=[], bool=False):
        self.name = name
        self.accepted_values = [True, False] if bool else [None, *accepted_values]
        self.value = ""
        self.bool = bool

    def validate(self, value: str):
        value = value.lower() if type(value) is str else value
        self.value = value == "true" if self.bool else value
        is_valid = self.value in self.accepted_values
        return is_valid

    def __repr__(self) -> str:
        return self.name


class BaseAPIView(generics.GenericAPIView):
    """Base for all indietour views.

    Path variables are automatically assigned to serializer context."""

    def initial(self, request, *args, **kwargs):
        self.validate_query_params()
        return super().initial(request, *args, **kwargs)

    query_params: list[QueryParam] = []
    """Add QueryParams expected for this view"""
    validated_query_params: dict[str, str] = {}
    """dict containing python-validated query params"""

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
        context.update(self.validated_query_params)
        return context

    def get_bands_for_user(self):
        user = self.request.user
        bands = Band.objects.filter(Q(owner=user) | Q(bandusers__user=user)).order_by("name")
        archived_bands = self.validated_query_params.get("archived_bands")
        if not archived_bands:
            bands = bands.filter(is_archived=False)
        return bands

    def user_bands_response(self, status_code=200):
        bands = self.get_bands_for_user()
        ser = BandSerializer(bands, many=True, context=self.get_serializer_context())
        return Response(ser.data, status_code)

    def get_tours_for_band(self):
        band_id = self.kwargs.get("band_id")
        tours = Tour.objects.filter(band_id=band_id)
        archived_tours = self.validated_query_params.get("archived_tours")
        if not archived_tours:
            tours = tours.filter(is_archived=False)
        return tours

    def band_tours_response(self, status_code=200):
        tours = self.get_tours_for_band()
        ser = TourSerializer(tours, many=True, context=self.get_serializer_context())
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
