from rest_framework import serializers
from core.query_params import QueryParamsManager


class BaseSerializer(serializers.ModelSerializer):
    # default_error_messages = {"invalid": "could not validate"}
    query_params: QueryParamsManager

    def is_valid(self, *, raise_exception=True):
        request = self.context.get("request")
        self.user = request.user
        self.query_params = self.context.get("query_params")
        return super().is_valid(raise_exception=raise_exception)

    def get_fields(self):
        self.init_query_params()
        self.query_params: QueryParamsManager = self.context.get("query_params")
        self.query_params.set_serializer(self)
        return super().get_fields()

    def init_query_params(self):
        """Override to assign instance vars for any query params. Called with get_fields"""
        pass
