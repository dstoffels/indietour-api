from rest_framework.views import exception_handler
from rest_framework.response import Response
from django.core.exceptions import ValidationError


def globals(exc, context):
    response = exception_handler(exc, context)

    if isinstance(response, ValidationError):
        response = Response({"details": exc.messages[0], "code": exc.code}, 400)
    return response
