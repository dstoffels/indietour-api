from rest_framework.views import exception_handler
from rest_framework.response import Response


def globals(exc, context):
    print(type(exc))

    # standard view handling
    response = exception_handler(exc, context)
    if response:
        return response

    # handle django erros
    from django.core.exceptions import ValidationError

    if isinstance(exc, ValidationError):
        return Response({"detail": exc.messages, "code": exc.code}, 400)

    # handle rest_framework errors
    from rest_framework.exceptions import ValidationError

    if isinstance(exc, ValidationError):
        return Response(data={"detail": exc.detail}, status=400)

    raise exc
