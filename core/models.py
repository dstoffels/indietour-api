from django.db import models
import uuid
from django.http import Http404
from typing import TypeVar, Type


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


T = TypeVar("T", bound=models.Model)


def get_or_404(model: Type[T], *args, **kwargs) -> T:
    from django.shortcuts import get_object_or_404

    try:
        return get_object_or_404(model, *args, **kwargs)
    except:
        raise Http404(f"Invalid {model._meta.model_name.lower()}_id")
