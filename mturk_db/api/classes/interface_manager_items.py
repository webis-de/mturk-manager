from api.helpers import raise_not_implemented_exception
from api.models import Project
from rest_framework.request import Request
import json
from typing import Tuple


from django.db.models import QuerySet, Model


class Interface_Manager_Items(object):
    @staticmethod
    def get_all(database_object_project: Project, request: Request) -> Tuple[QuerySet, list]:
        """
        Args:
            database_object_project: The project
            request: The project
            fields: The project
        """
        raise_not_implemented_exception('get_all', __class__)

    @staticmethod
    def filter(queryset: QuerySet, request: Request) -> QuerySet:
        raise_not_implemented_exception('filter', __class__)

    @staticmethod
    def annotate(queryset: QuerySet) -> QuerySet:
        raise_not_implemented_exception('annotate', __class__)

    @staticmethod
    def sort_by(queryset: QuerySet, request: Request) -> QuerySet:
        sort_by = request.query_params.get('sort_by')

        if sort_by is not None:
            descending = request.query_params.get('descending', 'false') == 'true'
            queryset = queryset.order_by(
                ('-' if descending else '') + sort_by
            )

        return queryset

    @staticmethod
    def limit(queryset: QuerySet, request: Request) -> QuerySet:
        limit = request.query_params.get('limit')

        if limit is not None:
            queryset = queryset[:int(limit)]

        return queryset

    @staticmethod
    def fields(queryset: QuerySet, request: Request) -> QuerySet:
        list_fields = request.query_params.getlist('fields[]')
        if len(list_fields) > 0:
            queryset = queryset.values(
                *list_fields
            )

        return queryset, list_fields

    @staticmethod
    def get(id_item: object) -> object:
        raise_not_implemented_exception('get', __class__)

    @staticmethod
    def create(data: object) -> object:
        raise_not_implemented_exception('create', __class__)

    @staticmethod
    def update(instance: Model, data: dict) -> Model:
        raise_not_implemented_exception('update', __class__)

    @staticmethod
    def delete(id_item: int) -> None:
        raise_not_implemented_exception('delete', __class__)

    @staticmethod
    def filter_value(queryset: QuerySet, request: Request, name_filter: str, name_field: str, name_lookup: str = 'exact'):
        value = request.query_params.get(name_filter)
        if value is not None:
            if json.loads(request.query_params.get('{name_filter}Exclude'.format(name_filter=name_filter), 'false')):
                queryset = queryset.exclude(**{
                    '{}__{}'.format(name_field, name_lookup): value
                })
            else:
                queryset = queryset.filter(**{
                    '{}__{}'.format(name_field, name_lookup): value
                })

        return queryset

    @staticmethod
    def filter_boolean(queryset: QuerySet, request: Request, name_filter: str, name_field: str):
        isActive = json.loads(request.query_params.get(name_filter, 'false'))
        if isActive == True:
            if json.loads(request.query_params.get('{name_filter}Exclude'.format(name_filter=name_filter), 'false')):
                queryset = queryset.exclude(**{
                    name_field: True
                })
            else:
                queryset = queryset.filter(**{
                    name_field: True
                })

        return queryset
    # @staticmethod
    # def filter_boolean(queryset: QuerySet, request: Request, name_filter: str, name_field: str):
    #     value = request.query_params.get(name_filter)
    #     if value is not None:
    #         if json.loads(request.query_params.get('{name_filter}Exclude'.format(name_filter=name_filter), 'false')):
    #             queryset = queryset.exclude(**{
    #                 name_field: json.loads(value)
    #             })
    #         else:
    #             queryset = queryset.filter(**{
    #                 name_field: json.loads(value)
    #             })
    #
    #     return queryset

    #
    @staticmethod
    def filter_list(queryset: QuerySet, request: Request, name_filter: str, name_field: str) -> QuerySet:
        items_selected = request.query_params.getlist('{name_filter}[]'.format(name_filter=name_filter))
        items_selected = [name.upper() for name in items_selected]

        if len(items_selected) > 0:
            if json.loads(request.query_params.get('{name_filter}Exclude'.format(name_filter=name_filter), 'false')):
                queryset = queryset.exclude(**{
                    '{name_field}__in'.format(name_field=name_field): items_selected
                })
            else:
                queryset = queryset.filter(**{
                    '{name_field}__in'.format(name_field=name_field): items_selected
                })

        return queryset.distinct()
