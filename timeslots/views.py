from rest_framework import generics
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import ValidationError
from .serializers import Timeslot, TimeslotSerializer
from tours.serializers import Tour, TourSerializer
from dates.serializers import Date, DateSerializer
from tours.permissions import IsTourUser, IsTourAdmin, IsBandUser
from bands.permissions import IsBandAdmin
from django.shortcuts import get_object_or_404


class TimeslotsView(generics.CreateAPIView):
    serializer_class = TimeslotSerializer
    permission_classes = (IsTourAdmin,)

    def post(self, request: Request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        tour = get_object_or_404(Tour, id=kwargs.get("tour_id"))
        return Response(TourSerializer(tour).data)

    # def perform_create(self, serializer: TimeslotSerializer):
    #     # serializer.context.update(self.kwargs)
    #     date_id = self.kwargs.get("date_id")
    #     serializer.save(date_id=date_id)
    #     return super().perform_create(serializer)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(self.kwargs)
        return context


class TimeslotView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Timeslot.objects.all()
    serializer_class = TimeslotSerializer
    permission_classes = (IsTourAdmin,)
    lookup_url_kwarg = "timeslot_id"
    lookup_field = "id"

    def patch(self, request, *args, **kwargs):
        super().patch(request, *args, **kwargs)
        tour = get_object_or_404(Tour, id=kwargs.get("tour_id"))
        return Response(TourSerializer(tour).data)

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        tour = get_object_or_404(Tour, id=kwargs.get("tour_id"))
        return Response(TourSerializer(tour).data)
