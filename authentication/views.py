from django.shortcuts import render
from rest_framework import generics
from .serializers import RegistrationSerializer
from rest_framework.permissions import AllowAny


class RegisterView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
