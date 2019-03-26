import json

from django.db.models import Count, F, QuerySet
from rest_framework.request import Request

from api.classes import Interface_Manager_Items
from api.models import HIT


class Manager_HITs(Interface_Manager_Items):
    @staticmethod
    def get_all(database_object_project, request, fields=None, use_sandbox=None):
        queryset = HIT.objects.filter(
            batch__project=database_object_project,
            batch__use_sandbox=use_sandbox,
        )

        queryset = Manager_HITs.filter(
            queryset=queryset,
            request=request
        )

        queryset = Manager_HITs.annotate(queryset)

        queryset = Manager_HITs.sort_by(
            queryset=queryset,
            request=request
        )

        if fields is not None:
            queryset = queryset.values(
                *fields
            )

        return queryset

    @staticmethod
    def filter(queryset: QuerySet, request: Request) -> QuerySet:
        list_ids = json.loads(request.query_params.get('list_ids', '[]'))

        if len(list_ids) > 0:
            queryset = HIT.objects.filter(
                id__in=list_ids
            )

        id_batch = request.query_params.get('id_batch')
        if id_batch is not None:
            queryset = queryset.filter(
                batch__id=id_batch,
            )

        hits_selected = request.query_params.getlist('hitsSelected[]')
        hits_selected = [name.upper() for name in hits_selected]

        if len(hits_selected) > 0:
            queryset = queryset.filter(id_hit__in=hits_selected)

        return queryset

    @staticmethod
    def annotate(queryset: QuerySet) -> QuerySet:
        return queryset.annotate(
            count_assignments_available=Count('assignments', distint=True),
            count_assignments_total=F('batch__settings_batch__count_assignments'),
        )

    @staticmethod
    def sort_by(queryset: QuerySet, request: Request) -> QuerySet:
        sort_by = request.query_params.get('sort_by')

        if sort_by is not None:
            if sort_by == 'batch':
                sort_by = 'batch__name'

            descending = request.query_params.get('descending', 'false') == 'true'
            queryset = queryset.order_by(
                ('-' if descending else '') + sort_by
            )

        return queryset
