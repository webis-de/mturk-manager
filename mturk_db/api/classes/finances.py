from django.db.models import F, Count, Q, Sum, Max, Min, Case, When, Value, IntegerField
from django.db.models.functions import Coalesce
import json
from api.enums import assignments
from api.classes import Manager_Projects, Manager_Assignments, Manager_HITs, Manager_Batches
from api.models import Batch
from datetime import datetime


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
    def aggregate_batches(cls, queryset):
        now = datetime.now()

        return queryset.annotate(
            count_assignments_living_total=Coalesce(Count(
                'hits__assignments',
                distinct=True,
                filter=Q(hits__datetime_expiration__gt=now)
            ), 0),
            count_assignments_living_available=Coalesce(Count(
                'hits__assignments',
                distinct=True,
                filter=Q(hits__datetime_expiration__gt=now) & Q(hits__assignments__status_external__isnull=False)
            ), 0)
        ).annotate(
            count_assignments_potential=F('count_assignments_living_total') - F('count_assignments_living_available'),

            count_assignments_approved=Coalesce(Count(
                'hits__assignments',
                distinct=True,
                filter=Q(hits__assignments__status_external=assignments.STATUS_EXTERNAL.APPROVED)
            ), 0),
        ).annotate(
            costs_so_far=F('count_assignments_approved') * F('settings_batch__reward'),
            costs_pending=F('count_assignments_potential') * F('settings_batch__reward')
        ).aggregate(
            sum_costs_so_far=Coalesce(Sum('costs_so_far'), 0),
            sum_costs_pending=Coalesce(Sum('costs_pending'), 0),
        )

    @classmethod
    def aggregate_hits(cls, queryset):
        now = datetime.now()

        return queryset.annotate(
            count_assignments_approved=Coalesce(Count(
                'assignments',
                distinct=True,
                filter=Q(assignments__status_external=assignments.STATUS_EXTERNAL.APPROVED)
            ), 0),
            count_assignments_potential=Case(
                When(datetime_expiration__gt=now,
                     then=F('batch__settings_batch__count_assignments') - Count(
                            'assignments',
                            filter=Q(assignments__status_external__isnull=False),
                            distinct=True
                     )
                 ),
                default=Value(0),
                output_field=IntegerField()
            )
        ).annotate(
            costs_so_far=F('count_assignments_approved') * F('batch__settings_batch__reward'),
            costs_pending=F('count_assignments_potential') * F('batch__settings_batch__reward'),
        ).aggregate(
            sum_costs_so_far=Coalesce(Sum('costs_so_far'), 0),
            sum_costs_pending=Coalesce(Sum('costs_pending'), 0),
        )

    @classmethod
    def aggregate_assignments(cls, queryset):
        return queryset.aggregate(
            sum_costs_so_far=Coalesce(Sum(
                'hit__batch__settings_batch__reward',
                distinct=True,
                filter=Q(status_external=assignments.STATUS_EXTERNAL.APPROVED)
            ), 0),
            sum_costs_pending=Coalesce(Sum(
                'hit__batch__settings_batch__reward',
                distinct=True,
                filter=Q(status_external=None)
            ), 0)
        )

    @staticmethod
    def get_balance(database_object_project, use_sandbox):
        client = Manager_Projects.get_mturk_api(use_sandbox)
        return {
            'balance': float(client.get_account_balance()['AvailableBalance'])
        }