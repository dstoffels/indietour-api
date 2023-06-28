from rest_framework import serializers


class BaseSerializer(serializers.ModelSerializer):
    default_error_messages = {"invalid": "could not validate"}

    def is_valid(self, *, raise_exception=True):
        request = self.context.get("request")
        self.user = request.user
        return super().is_valid(raise_exception=raise_exception)

    def validate(self, attrs):
        self.context
        return super().validate(attrs)
