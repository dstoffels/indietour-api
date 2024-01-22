from rest_framework import generics
from rest_framework.request import Request
from .serializers import Show, ShowSerializer
from tours.permissions import IsTourUser, IsTourAdmin
from core.views import BaseAPIView
from rest_framework.response import Response
from .status_choices import STATUS_CHOICES


class ShowsView(generics.ListCreateAPIView, BaseAPIView):
    serializer_class = ShowSerializer
    permission_classes = (IsTourUser,)

    def get_queryset(self):
        return Show.objects.filter(date_id=self.path_vars.date_id)


class ShowView(generics.RetrieveUpdateDestroyAPIView, BaseAPIView):
    model = Show
    serializer_class = ShowSerializer
    lookup_field = "id"
    lookup_url_kwarg = "show_id"

    def get_permissions(self):
        if self.request.method == "GET":
            return (IsTourUser(),)
        return (IsTourAdmin(),)


class ShowStatusView(generics.RetrieveAPIView, BaseAPIView):
    def get(self, request, *args, **kwargs):
        return Response(data=STATUS_CHOICES)
