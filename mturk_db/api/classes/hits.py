import json

from django.db.models import Count, F, QuerySet, Q, Sum, Case, When, Value, IntegerField
from django.db.models.functions import Coalesce
from rest_framework.request import Request
from api.enums import assignments
from api.classes import Interface_Manager_Items
from api.models import HIT
from django.utils import timezone


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

        queryset = Manager_HITs.filter_list(
            queryset=queryset,
            request=request,
            name_filter='hitsSelected',
            name_field='id_hit'
        )

        queryset = Manager_HITs.filter_list(
            queryset=queryset,
            request=request,
            name_filter='batchesSelected',
            name_field='batch__name'
        )

        return queryset

    @staticmethod
    def annotate(queryset: QuerySet) -> QuerySet:
        now = timezone.now()

        return queryset.annotate(
            count_assignments_total=F('batch__settings_batch__count_assignments'),

            count_assignments_approved=Coalesce(Count(
                'assignments',
                distinct=True,
                filter=Q(assignments__status_external=assignments.STATUS_EXTERNAL.APPROVED)
            ), 0),

            count_assignments_rejected=Coalesce(Count(
                'assignments',
                distinct=True,
                filter=Q(assignments__status_external=assignments.STATUS_EXTERNAL.REJECTED)
            ), 0),

            count_assignments_submitted=Coalesce(Count(
                'assignments',
                distinct=True,
                filter=Q(assignments__status_external__isnull=True)
            ), 0),

            count_assignments_pending=Case(
                When(datetime_expiration__gt=now,
                     then=F('batch__settings_batch__count_assignments') - Count(
                            'assignments',
                            distinct=True
                     )
                 ),
                default=Value(0),
                output_field=IntegerField()
            )
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
