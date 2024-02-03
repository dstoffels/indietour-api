from rest_framework import serializers
from core.query_params import QueryParamsManager
from core.path_vars import PathVars
from authentication.models import User


class BaseSerializer(serializers.ModelSerializer):
    parent_url_kwarg = ""
    query_params: QueryParamsManager

    def is_valid(self, *, raise_exception=True):
        request = self.context.get("request")
        self.user: User = request.user
        self.query_params = self.context.get("query_params")
        return super().is_valid(raise_exception=raise_exception)

    def get_fields(self):
        request = self.context.get("request")
        self.user = request.user
        self.init_query_params()
        self.path_vars: PathVars = self.context.get("path_vars")
        self.path_vars.to_obj_attrs(self)

        self.query_params: QueryParamsManager = self.context.get("query_params")
        if isinstance(self.query_params, QueryParamsManager):
            self.query_params.to_obj_attrs(self)
        return super().get_fields()

    def create(self, validated_data):
        parent_id = self.path_vars.get(self.parent_url_kwarg)
        if parent_id:
            validated_data[self.parent_url_kwarg] = parent_id
        return super().create(validated_data)

    def init_query_params(self):
        """(OPTIONAL) Override to create instance vars for QueryParams. This is for intellisense only, vars must not be assigned a value. Called first in self.get_fields()

        Syntax: self.instance_var: QueryParam
        """
        pass
