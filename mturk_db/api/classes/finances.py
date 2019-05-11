from botocore.exceptions import EndpointConnectionError
from django.db.models import F, Count, Q, Sum, Max, Min, Case, When, Value, IntegerField, OuterRef, Subquery, \
    ExpressionWrapper
from django.db.models.functions import Coalesce
import json
from api.enums import assignments
from api.classes import Manager_Projects, Manager_Assignments, Manager_HITs, Manager_Batches
from api.models import Batch, HIT
from django.utils import timezone


class ManagerFinances(object):
    items = {
        'assignments': Manager_Assignments,
        'hits': Manager_HITs,
        'batches': Manager_Batches
    }

    @classmethod
    def get(cls, database_object_project, use_sandbox, request):
        type_item = request.query_params.get('typeItem')

        manager = cls.items[type_item]

        queryset = manager.get_all(
            database_object_project=database_object_project,
            request=request,
            use_sandbox=use_sandbox
        )

        if type_item == 'batches':
            queryset = ManagerFinances.aggregate_batches(
                queryset=queryset
            )
        elif type_item == 'hits':
            queryset = ManagerFinances.aggregate_hits(
                queryset=queryset
            )
        elif type_item == 'assignments':
            queryset = ManagerFinances.aggregate_assignments(
                queryset=queryset
            )

        return queryset

    @classmethod
    def aggregate_batches(cls, queryset) -> dict:
        queryset = Manager_Batches.annotate_assignments(queryset)

        return queryset.annotate(
            costs_approved=ExpressionWrapper(
                F('count_assignments_approved') * F('settings_batch__reward'), output_field=IntegerField()
            ),
            costs_rejected=ExpressionWrapper(
                F('count_assignments_rejected') * F('settings_batch__reward'), output_field=IntegerField()
            ),
            costs_submitted=ExpressionWrapper(
                F('count_assignments_submitted') * F('settings_batch__reward'), output_field=IntegerField()
            ),
            costs_dead=ExpressionWrapper(
                F('count_assignments_dead') * F('settings_batch__reward'), output_field=IntegerField()
            ),
            costs_pending=ExpressionWrapper(
                F('count_assignments_pending') * F('settings_batch__reward'), output_field=IntegerField()
            ),
        ).aggregate(
            sum_costs_approved=Coalesce(Sum('costs_approved'), 0),
            sum_costs_rejected=Coalesce(Sum('costs_rejected'), 0),
            sum_costs_submitted=Coalesce(Sum('costs_submitted'), 0),
            sum_costs_dead=Coalesce(Sum('costs_dead'), 0),
            sum_costs_pending=Coalesce(Sum('costs_pending'), 0),
        )

    @classmethod
    def aggregate_hits(cls, queryset) -> dict:
        queryset = Manager_HITs.annotate_assignments(queryset)

        return queryset.annotate(
            costs_approved=F('count_assignments_approved') * F('batch__settings_batch__reward'),
            costs_rejected=F('count_assignments_rejected') * F('batch__settings_batch__reward'),
            costs_submitted=F('count_assignments_submitted') * F('batch__settings_batch__reward'),
            costs_dead=F('count_assignments_dead') * F('batch__settings_batch__reward'),
            costs_pending=F('count_assignments_pending') * F('batch__settings_batch__reward')
        ).aggregate(
            sum_costs_approved=Coalesce(Sum('costs_approved'), 0),
            sum_costs_rejected=Coalesce(Sum('costs_rejected'), 0),
            sum_costs_submitted=Coalesce(Sum('costs_submitted'), 0),
            sum_costs_dead=Coalesce(Sum('costs_dead'), 0),
            sum_costs_pending=Coalesce(Sum('costs_pending'), 0),
        )

    @classmethod
    def aggregate_assignments(cls, queryset) -> dict:
        return queryset.aggregate(
            sum_costs_approved=Coalesce(Sum(
                'hit__batch__settings_batch__reward',
                # distinct=True,
                filter=Q(status_external=assignments.STATUS_EXTERNAL.APPROVED)
            ), 0),
            sum_costs_rejected=Coalesce(Sum(
                'hit__batch__settings_batch__reward',
                # distinct=True,
                filter=Q(status_external=assignments.STATUS_EXTERNAL.REJECTED)
            ), 0),
            sum_costs_submitted=Coalesce(Sum(
                'hit__batch__settings_batch__reward',
                # distinct=True,
                filter=Q(status_external__isnull=True)
            ), 0)
        )

    @staticmethod
    def get_balance(use_sandbox: bool) -> dict:
        client = Manager_Projects.get_mturk_api(use_sandbox)
        try:
            balance = float(client.get_account_balance()['AvailableBalance'])
        except EndpointConnectionError:
            balance = None

        return {
            'balance': balance
        }