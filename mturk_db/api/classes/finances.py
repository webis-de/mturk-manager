from django.db.models import F, Count, Q, Sum, Max, Min
from django.db.models.functions import Coalesce

from api.enums import assignments
from api.classes import Manager_Projects
from api.models import Batch
from datetime import datetime


class ManagerFinances(object):
    @classmethod
    def get(cls, database_object_project, use_sandbox, request):
        now = datetime.now()
        batches = Batch.objects.filter(
            project=database_object_project,
            use_sandbox=use_sandbox,
        ).annotate(
            # number of living hits of each batch
            count_hits_total=Count('hits', distint=True),
            count_hits_living=Count('hits', distint=True, filter=Q(hits__datetime_expiration__gt=now)),
            count_hits_expired=Count('hits', distint=True, filter=Q(hits__datetime_expiration__lte=now)),

            # number of processed assignments
            count_assignments_available=Coalesce(Count('hits__assignments', distinct=True), 0)
        ).annotate(
            count_assignments_total=F('count_hits_total') * F('settings_batch__count_assignments'),
            count_assignments_approved=Coalesce(Count(
                'hits__assignments',
                distinct=True,
                filter=Q(hits__assignments__status_external=assignments.STATUS_EXTERNAL.APPROVED)
            ), 0),
            count_assignments_rejected=Coalesce(Count(
                'hits__assignments',
                distinct=True,
                filter=Q(hits__assignments__status_external=assignments.STATUS_EXTERNAL.REJECTED)
            ), 0),
        ).annotate(
            costs_max=F('count_assignments_total') * F('settings_batch__reward'),
            costs_so_far=F('count_assignments_approved') * F('settings_batch__reward'),
        ).aggregate(
            sum_costs_max=Coalesce(Sum('costs_max'), 0),
            # max_costs_max=Coalesce(Max('costs_max'), 0),
            # min_costs_max=Coalesce(Min('costs_max'), 0),

            sum_costs_so_far=Coalesce(Sum('costs_so_far'), 0),
            # max_costs_so_far=Coalesce(Max('costs_so_far'), 0),
            # min_costs_so_far=Coalesce(Min('costs_so_far'), 0),
        )

        return batches

    @staticmethod
    def get_balance(database_object_project, use_sandbox):
        client = Manager_Projects.get_mturk_api(use_sandbox)
        return {
            'balance': float(client.get_account_balance()['AvailableBalance'])
        }