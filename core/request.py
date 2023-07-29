from django.core.handlers.wsgi import WSGIRequest
from django.urls import resolve
from django.shortcuts import get_object_or_404
from bands.models import Band
from tours.models import Tour


class Request(WSGIRequest):
    def __init__(self, environ) -> None:
        super().__init__(environ)
        self.band: Band = None
        self.tour: Tour = None

        match = resolve(self.path_info)

        band_id = match.kwargs.get("band_id", None)
        if band_id:
            self.band = get_object_or_404(Band, id=band_id)

        tour_id = match.kwargs.get("tour_id", None)
        if tour_id:
            self.tour = get_object_or_404(Tour, id=tour_id)
            self.band = self.tour.band
