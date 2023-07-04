import os
import requests
from rest_framework.exceptions import ValidationError

GAPI_BASE_URL = "https://maps.googleapis.com/maps/api"


def fetch_place(place_id):
    response = requests.get(
        f'{GAPI_BASE_URL}/place/details/json?key={os.getenv("GOOGLE_API_KEY")}&place_id={place_id}&fields=place_id,formatted_address,geometry,name,address_components,type,editorial_summary,business_status'
    )
    response = response.json()
    status = response.get("status")
    if status == "INVALID_REQUEST":
        raise ValidationError(response)

    return response.get("result")
