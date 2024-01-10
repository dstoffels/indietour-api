from django.http import Http404
from django.db import models


def retrieve_or_404(model: models.Model, id):
    try:
        return model.objects.get(id=id)
    except model.DoesNotExist:
        raise Http404(f"The {model.__name__} with the provided id does not exist.")
