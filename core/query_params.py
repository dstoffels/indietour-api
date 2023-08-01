from rest_framework.request import Request
from rest_framework.exceptions import ValidationError
from django.utils.dateparse import parse_datetime


class QueryParam:
    def __init__(self, name: str, accepted_values: list[str] = [], required=False):
        self.name = name
        self.value: str = None
        self.accepted_values = accepted_values
        self.required = required

    def set_value(self, value: str):
        self.value = value

    def validate_value(self):
        return self.is_null() or not bool(self.accepted_values) or self.value in self.accepted_values

    def is_valid(self):
        if self.required and self.value is None:
            raise ValidationError({"detail": f"{self.name} is a required query param."})

        return not bool(self.accepted_values) or self.value in self.accepted_values

    def is_invalid(self):
        return not self.is_valid()

    def contains(self, value):
        return self.value == value

    def is_null(self):
        return self.value is None

    def __repr__(self) -> str:
        return f"QueryParam <{self.name}: {self.value}>"


class BooleanQueryParam(QueryParam):
    def __init__(self, name: str):
        super().__init__(name, [True, False])

    def set_value(self, value: str):
        super().set_value(value)
        self.value = self.value == "true"

    def is_valid(self):
        super().is_valid()
        return self.value


class ListQueryParam(QueryParam):
    def set_value(self, value: str):
        super().set_value(value)
        if not self.is_null():
            self.value = self.value.replace(" ", "").split(",")

    def contains(self, value):
        return not self.is_null() and value in self.value

    def validate_value(self):
        return self.is_null() or bool(set(self.value) & set(self.accepted_values))

    def has_values(self):
        return not self.is_null() and bool(len(self.value))


class DateTimeQueryParam(QueryParam):
    def set_value(self, value: str):
        if value is not None:
            try:
                self.value = parse_datetime(value).replace(hour=23, minute=59, second=59)
            except:
                raise ValidationError({"detail": f"{self.name} must be an ISO datetime format. Value: {value}"})


class QueryParamsManager:
    def __init__(self, query_params: list[QueryParam], request: Request) -> None:
        self.query_params = query_params
        self.request = request
        self.validated_query_params: dict[str, QueryParam] = {}
        self.__set_values()
        self.validate()

    def validate(self):
        invalid_params: list[QueryParam] = []
        for param in self.query_params:
            if param.value is not None:
                if not param.validate_value():
                    invalid_params.append(param)

        if len(invalid_params):
            raise ValidationError(
                {
                    "detail": "Invalid query parameter value(s)",
                    "invalid_params": [
                        {param.name: param.value, "accepted values": param.accepted_values} for param in invalid_params
                    ],
                }
            )

    def update_context(self, context: dict):
        """Adds itself to a serializer's context["query_params"]"""
        context.update({"query_params": self})
        return context

    def to_obj_attrs(self, obj):
        for param in self.query_params:
            setattr(obj, param.name, param)

    def get(self, param_name: str):
        return next((param for param in self.query_params if param.name == param_name), None)

    def __set_values(self):
        for param in self.query_params:
            param.set_value(self.request.query_params.get(param.name))

    def __repr__(self) -> str:
        return [f"{param.name}: {param.value}" for param in self.query_params]
