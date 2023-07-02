from rest_framework.views import exception_handler
from rest_framework.response import Response
from django.core.exceptions import ValidationError


def globals(exc, context):
    response = exception_handler(exc, context)
    if response:
        if isinstance(response, ValidationError):
            response = Response({"details": exc.messages, "code": exc.code}, 400)
        return response

    if isinstance(exc, AttributeError):
        response = Response({"errors": exc.args}, 500)
    return Response(exc.args)
