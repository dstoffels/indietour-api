from django.core.handlers.wsgi import WSGIRequest
from .request import Request


class RequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: WSGIRequest):
        if request.path_info.startswith("/admin"):
            return self.get_response(request)

        request = Request(request.environ)
        return self.get_response(request)
