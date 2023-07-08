from rest_framework import generics
from rest_framework.request import Request
from .serializers import Date, DateSerializer, Show, ShowSerializer
from tours.permissions import IsTourUser, IsTourAdmin
from core.views import BaseAPIView
from core.query_params import ListQueryParam, BooleanQueryParam, QueryParam
from datetime import date
from contacts.serializers import Contact, ContactSerializer


class BaseDatesView(BaseAPIView):
    def get_query_params(self) -> list[QueryParam]:
        return [
            ListQueryParam("include", ["all", "timeslots", "contacts", "prospects", "lodgings"]),
            BooleanQueryParam("past_dates"),
        ]


class DatesView(generics.ListCreateAPIView, BaseDatesView):
    serializer_class = DateSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return (IsTourUser(),)
        return (IsTourAdmin(),)

    def get_queryset(self):
        tourdates = Date.objects.filter(tour_id=self.kwargs.get("tour_id")).order_by("date")
        if self.past_dates.is_invalid():
            tourdates = tourdates.filter(date__gte=date.today())
        return tourdates

    def init_query_params(self, request: Request):
        super().init_query_params(request)
        self.include: ListQueryParam
        self.past_dates: BooleanQueryParam


class DateView(generics.RetrieveUpdateDestroyAPIView, BaseDatesView):
    queryset = Date.objects.all()
    serializer_class = DateSerializer
    lookup_field = "id"
    lookup_url_kwarg = "date_id"

    def get_permissions(self):
        if self.request.method == "GET":
            return (IsTourUser(),)
        return (IsTourAdmin(),)


class DateContactsView(generics.CreateAPIView, BaseDatesView):
    serializer_class = ContactSerializer

    def post(self, request: Request, *args, **kwargs):
        ser = ContactSerializer(data=request.data, context=self.get_serializer_context())
        ser.is_valid()
        ser.save()
        date = Date.objects.filter(id=self.path_vars.date_id).first()
        date.contacts.add(ser.instance)
        date.save()
        return self.date_response()


class ShowsView(generics.ListCreateAPIView, BaseDatesView):
    serializer_class = ShowSerializer

    def get_queryset(self):
        return Show.objects.filter(date_id=self.path_vars.date_id)
