from rest_framework import generics


class BaseAPIView(generics.GenericAPIView):
    """Base for all indietour views.

    Path variables are automatically assigned to serializer context."""

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(self.kwargs)
        return context
