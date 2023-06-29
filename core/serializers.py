from rest_framework import serializers
from rest_framework.fields import empty


class BaseSerializer(serializers.ModelSerializer):
    default_error_messages = {"invalid": "could not validate"}
    query_params = {}

    def is_valid(self, *, raise_exception=True):
        request = self.context.get("request")
        self.user = request.user
        return super().is_valid(raise_exception=raise_exception)

    def get_fields(self):
        print(self.request)
        self.query_params = self.context.get("query_params")
        return super().get_fields()
