from rest_framework import serializers
from .models import Place
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from .utils import fetch_place


class PlaceSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    formatted_address = serializers.CharField(read_only=True)
    political_address = serializers.CharField(read_only=True)
    lat = serializers.DecimalField(max_digits=13, decimal_places=10, read_only=True)
    lng = serializers.DecimalField(max_digits=13, decimal_places=10, read_only=True)

    class Meta:
        model = Place
        fields = "__all__"

    def create(self, validated_data):
        place_id = self.initial_data.get("place_id")
        place, created = Place.objects.get_or_create(id=place_id)

        if created:
            result = fetch_place(place_id)
            address_components = result.get("address_components")

            political_address = []

            locality = next((comp["short_name"] for comp in address_components if "locality" in comp["types"]), None)
            if locality:
                political_address.append(locality)

            admin_area = next(
                (comp["short_name"] for comp in address_components if "administrative_area_level_1" in comp["types"]),
                None,
            )
            if admin_area:
                political_address.append(admin_area)

            country = next((comp["short_name"] for comp in address_components if "country" in comp["types"]), None)
            if country:
                political_address.append(country)

            political_address = ", ".join(political_address)

            place.formatted_address = result.get("formatted_address")
            place.name = result.get("name")
            place.lat = result.get("geometry", {}).get("location", {}).get("lat")
            place.lng = result.get("geometry", {}).get("location", {}).get("lng")
            place.political_address = political_address

            place.save()

        return place
