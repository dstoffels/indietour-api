from rest_framework import generics
from rest_framework.exceptions import ValidationError
from bands.serializers import Band, BandSerializer
from tours.serializers import Tour, TourSerializer
from dates.serializers import Date, DateSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response


class BaseAPIView(generics.GenericAPIView):
    """Base for all indietour views.

    Path variables are automatically assigned to serializer context."""

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(self.kwargs)
        return context

    def band_response(self, status_code=200):
        band = get_object_or_404(Band, id=self.kwargs.get("band_id"))
        return Response(BandSerializer(band).data, status_code)

    def tour_response(self, status_code=200):
        tour = get_object_or_404(Tour, id=self.kwargs.get("tour_id"))
        return Response(TourSerializer(tour).data, status_code)


class BandDependentView(BaseAPIView):
    def initial(self, request, *args, **kwargs):
        try:
            obj = self.get_object()
            self.validate_band(obj, **kwargs)
        except:
            pass
        return super().initial(request, *args, **kwargs)

    def validate_band(self, band_dependend_obj, **kwargs):
        band_id = kwargs.get("band_id")
        if str(band_dependend_obj.band.id) != band_id:
            raise ValidationError(
                {
                    "details": f"{band_dependend_obj} does not belong to the provided band. band_id: {band_id}",
                    "code": "invalid",
                }
            )


class TourDependentView(BandDependentView):
    def initial(self, request, *args, **kwargs):
        try:
            obj = self.get_object()
            self.validate_tour(obj, **kwargs)
            self.validate_band(obj.tour, **kwargs)
        except:
            tour_id = kwargs.get("tour_id")
            tour = Tour.objects.only("band_id").get(id=tour_id)
            self.validate_band(tour, **kwargs)

        return super().initial(request, *args, **kwargs)

    def validate_tour(self, tour_dependent_obj, **kwargs):
        tour_id = kwargs.get("tour_id")
        if str(tour_dependent_obj.tour.id) != tour_id:
            raise ValidationError(
                {
                    "details": f"{tour_dependent_obj} does not belong to the provided tour. tour_id {tour_id}",
                    "code": "invalid",
                }
            )


class DateDependentView(TourDependentView):
    def initial(self, request, *args, **kwargs):
        try:
            obj = self.get_object()
            self.validated_date(obj, **kwargs)
            self.validate_tour(obj.date, **kwargs)
            self.validate_band(obj.date.tour, **kwargs)
        except:
            date_id = kwargs.get("date_id")
            date = Date.objects.only("tour_id").get(id=date_id)
            self.validate_tour(date, **kwargs)
        return super().initial(request, *args, **kwargs)

    def validated_date(self, date_dependent_obj, **kwargs):
        date_id = kwargs.get("date_id")
        if str(date_dependent_obj.date.id) != date_id:
            raise ValidationError(
                {
                    "details": f"{date_dependent_obj} does not belong to the provided date. date_id: {date_id}",
                    "code": "invalid",
                }
            )
