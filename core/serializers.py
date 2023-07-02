from rest_framework import serializers
from core.query_params import QueryParamsManager
from typing import Optional


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
        self.query_params = self.context.get("query_params")
        if isinstance(self.query_params, QueryParamsManager):
            self.query_params.set_to_obj_attrs(self)
        return super().get_fields()

    def init_query_params(self):
        """(OPTIONAL) Override to create instance vars for QueryParams. This is for intellisense only, vars must not be assigned a value. Called first in self.get_fields()

        Syntax: self.instance_var: QueryParam
        """
        pass
