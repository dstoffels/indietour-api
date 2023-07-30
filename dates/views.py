from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from .serializers import Date, DateSerializer, LogEntry, LogEntrySerializer
from tours.permissions import IsTourUser, IsTourAdmin
from core.views import BaseAPIView
from core.query_params import ListQueryParam, BooleanQueryParam, QueryParam
from datetime import date
from contacts.serializers import Contact, ContactSerializer


class BaseDatesView(BaseAPIView):
    def get_query_params(self) -> list[QueryParam]:
        return [
            ListQueryParam("include", ["all", "timeslots", "contacts", "shows", "lodgings"]),
            BooleanQueryParam("past_dates"),
            ListQueryParam("status", [choice.lower() for choice in Date.STATUS_CHOICES]),
        ]

    def get_permissions(self):
        if self.request.method == "GET":
            return (IsTourUser(),)
        return (IsTourAdmin(),)


class DatesView(generics.ListCreateAPIView, BaseDatesView):
    serializer_class = DateSerializer

    def get_queryset(self):
        tourdates = Date.objects.filter(tour_id=self.path_vars.tour_id).order_by("date")
        if self.past_dates.is_invalid():
            tourdates = tourdates.filter(date__gte=date.today())
        if self.status.has_values():
            tourdates = tourdates.filter(status__in=self.status.value)
        return tourdates

    def init_query_params(self, request: Request):
        super().init_query_params(request)
        self.include: ListQueryParam
        self.past_dates: BooleanQueryParam
        self.status: ListQueryParam


class DateView(BaseDatesView, generics.RetrieveUpdateDestroyAPIView):
    model = Date
    serializer_class = DateSerializer
    lookup_field = "id"
    lookup_url_kwarg = "date_id"


class DateContactView(generics.DestroyAPIView, generics.CreateAPIView, BaseDatesView):
    permission_classes = (IsTourAdmin,)

    def post(self, request: Request, *args, **kwargs):
        date = Date.objects.filter(id=self.path_vars.date_id).first()
        contact = Contact.objects.filter(id=self.path_vars.contact_id).first()
        if contact and not date.contacts.contains(contact):
            date.contacts.add(contact)
        return self.date_response()

    def delete(self, request, *args, **kwargs):
        date = Date.objects.filter(id=self.path_vars.date_id).first()
        contact = Contact.objects.filter(id=self.path_vars.contact_id).first()
        date.contacts.remove(contact)
        return self.date_response()


class DateLogView(generics.ListCreateAPIView, BaseAPIView):
    serializer_class = LogEntrySerializer

    def get_queryset(self):
        return LogEntry.objects.filter(date_id=self.path_vars.date_id).order_by("timestamp")


class LogEntryView(generics.RetrieveUpdateDestroyAPIView, BaseAPIView):
    model = LogEntry
    serializer_class = LogEntrySerializer
    lookup_field = "id"
    lookup_url_kwarg = "logentry_id"


class DateStatusView(generics.RetrieveAPIView, BaseAPIView):
    def get(self, request, *args, **kwargs):
        return Response(data=Date.STATUS_CHOICES)
