from rest_framework import serializers


class BaseSerializer(serializers.ModelSerializer):
    default_error_messages = {"invalid": "could not validate"}
    query_params: dict = {}

    def is_valid(self, *, raise_exception=True):
        request = self.context.get("request")
        self.user = request.user
        self.query_params = self.context.get("query_params")
        return super().is_valid(raise_exception=raise_exception)

    def get_fields(self):
        self.query_params = self.context.get("query_params")
        return super().get_fields()
