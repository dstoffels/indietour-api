import os
import requests

GAPI_BASE_URL = "https://maps.googleapis.com/maps/api"


def fetch_place(place_id):
    response = requests.get(
        f'{GAPI_BASE_URL}/place/details/json?key={os.getenv("GOOGLE_API_KEY")}&place_id={place_id}&fields=place_id,formatted_address,geometry,name,address_components'
    )
    return response.json().get("result")
