from rest_framework import generics
from rest_framework.request import Request
from .serializers import Date, DateSerializer
from tours.permissions import IsTourUser, IsTourAdmin
from core.views import BaseAPIView
from core.query_params import (
    ListQueryParam,
    BooleanQueryParam,
    QueryParam,
    DateQueryParam,
)
from contacts.serializers import Contact
from rest_framework.exceptions import ValidationError


class BaseDatesView(BaseAPIView):
    def get_query_params(self) -> list[QueryParam]:
        return [
            ListQueryParam(
                "include", ["all", "timeslots", "contacts", "shows", "lodgings"]
            ),
            BooleanQueryParam("past_dates"),
            BooleanQueryParam("all_dates"),
            DateQueryParam("request_date"),
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
            tourdates = tourdates.filter(date__gte=self.request_date.value)
        if self.all_dates.is_invalid():
            tourdates = tourdates.filter(is_published=True)

        return tourdates

    def init_query_params(self, request: Request):
        super().init_query_params(request)
        self.include: ListQueryParam
        self.past_dates: BooleanQueryParam
        self.all_dates: BooleanQueryParam
        self.request_date: DateQueryParam


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
