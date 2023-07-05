from rest_framework import serializers
from .models import Place
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from .utils import fetch_place


class PlaceSerializer(serializers.ModelSerializer):
    place_id = serializers.CharField(write_only=True)
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    formatted_address = serializers.CharField(read_only=True)
    political_address = serializers.CharField(read_only=True)
    lat = serializers.DecimalField(max_digits=13, decimal_places=10, read_only=True, coerce_to_string=False)
    lng = serializers.DecimalField(max_digits=13, decimal_places=10, read_only=True, coerce_to_string=False)
    overview = serializers.CharField(read_only=True)
    types = serializers.JSONField(read_only=True)
    business_status = serializers.CharField(read_only=True)
    website = serializers.CharField(read_only=True)

    class Meta:
        model = Place
        fields = "__all__"

    def create(self, validated_data):
        place_id = validated_data.get("place_id")
        place = Place.objects.filter(id=place_id).first()

        if not place:
            result: dict = fetch_place(place_id)

            name = result.get("name")
            lat = result.get("geometry", {}).get("location", {}).get("lat")
            lng = result.get("geometry", {}).get("location", {}).get("lng")

            overview = None
            summary = result.get("editorial_summary")
            if summary:
                overview = summary.get("overview")

            business_status = result.get("business_status")

            types = result.get("types")

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

            website = result.get("website")
            formatted_address = result.get("formatted_address")

            place = Place.objects.create(id=place_id)
            place.formatted_address = formatted_address
            place.name = name
            place.lat = lat
            place.lng = lng
            place.political_address = political_address
            place.overview = overview
            place.types = types
            place.business_status = business_status
            place.website = website

            place.save()

        return place

    def is_valid(self, *, raise_exception=True):
        return super().is_valid(raise_exception=raise_exception)
