class QueryParam:
    def __init__(self, name: str, accepted_values=[]):
        self.name = name
        self.accepted_values = accepted_values
        self.value: str = None

    def is_valid(self, value: str):
        self.value = value.lower()
        return self.value in self.accepted_values

    def __repr__(self) -> str:
        return f"QueryParam <{self.name}: {self.value}>"


class BooleanQueryParam(QueryParam):
    def __init__(self, name: str):
        super().__init__(name, [True, False])

    def is_valid(self, value: str):
        self.value = value.lower() == "true"
        return self.value in self.accepted_values


class ListQueryParam(QueryParam):
    def __init__(self, name: str, accepted_values=[]):
        super().__init__(name, accepted_values)

    def is_valid(self, value: str):
        self.value = value.split(",")
        for val in self.value:
            if val not in self.accepted_values:
                return False
        return True


from rest_framework.request import Request, HttpRequest
from rest_framework.exceptions import ValidationError


class QueryParamsManager:
    def __init__(self, query_params: list[QueryParam]) -> None:
        self.query_params = query_params
        self.validated_query_params: dict[str, QueryParam] = {}

    def validate(self, request: Request):
        invalid_params: list[QueryParam] = []
        for param in self.query_params:
            value = request.query_params.get(param.name)

            if value is not None:
                if not param.is_valid(value):
                    invalid_params.append(param)
                else:
                    self.validated_query_params.update({param.name: param})

        if len(invalid_params):
            raise ValidationError(
                {
                    "details": "Invalid query parameter value(s)",
                    "invalid_params": [
                        {param.name: param.value, "accepted values": param.accepted_values} for param in invalid_params
                    ],
                }
            )

    def update_context(self, context: dict):
        """Adds itself to a serializer context["query_params"]"""
        context.update({"query_params": self})
        return context

    def set_serializer(self, serializer):
        for param in self.validated_query_params.values():
            if hasattr(serializer, param.name):
                setattr(serializer, param.name, param.value)

    def get(self, param: str):
        return self.validated_query_params.get(param)

    def __repr__(self) -> str:
        return [f"{param.name}: {param.value}" for param in self.query_params]
