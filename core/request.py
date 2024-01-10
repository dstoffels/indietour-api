from django.core.handlers.wsgi import WSGIRequest
from django.urls import resolve
from django.shortcuts import get_object_or_404
from core.utils import retrieve_or_404
from bands.models import Band
from tours.models import Tour
from dates.models import Date
from shows.models import Show
from timeslots.models import Timeslot
from lodgings.models import Lodging
from core.models import UUIDModel


class Request(WSGIRequest):
    def __init__(self, environ) -> None:
        super().__init__(environ)
        self.kwargs = resolve(self.path_info).kwargs
        self.band: Band = self.set_resources(Band, "band_id")
        self.tour: Tour = self.set_resources(Tour, "tour_id")
        self.date: Date = self.set_resources(Date, "date_id")
        self.show: Show = self.set_resources(Show, "show_id")
        self.timeslot: Timeslot = self.set_resources(Timeslot, "timeslot_id")
        self.lodging: Lodging = self.set_resources(Lodging, "lodging_id")

    def set_resources(self, model: UUIDModel, kwarg: str):
        id = self.kwargs.get(kwarg)
        if id:
            obj = retrieve_or_404(model, id)
            returnObj = obj

            if hasattr(obj, "date") and not isinstance(obj, Date):
                obj: Date = obj.date
                self.date = obj

            if hasattr(obj, "tour"):
                obj: Tour = obj.tour
                self.tour = obj

            if hasattr(obj, "band"):
                self.band: Band = obj.band

            return returnObj
        return None
