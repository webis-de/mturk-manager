import json

from django.db.models import Count, F

from api.models import HIT


class Manager_HITs(object):
    @staticmethod
    def get_all(database_object_project, use_sandbox, request):
        list_ids = json.loads(request.query_params.get('list_ids', '[]'))

        queryset = HIT.objects.filter(
            batch__project=database_object_project,
            batch__use_sandbox=use_sandbox,
        )

        if len(list_ids) > 0:
            queryset = HIT.objects.filter(
                id__in=list_ids
            )

        id_batch = request.query_params.get('id_batch')
        if id_batch is not None:
            queryset = queryset.filter(
                batch__id=id_batch,
            )

        queryset = queryset.annotate(
            count_assignments_available=Count('assignments', distint=True),
            count_assignments_total=F('batch__settings_batch__count_assignments'),
        )

        sort_by = request.query_params.get('sort_by')
        if sort_by is not None:
            if sort_by == 'batch':
                sort_by = 'batch__name'

            descending = request.query_params.get('descending', 'false') == 'true'
            queryset = queryset.order_by(
                ('-' if descending else '') + sort_by
            )

        return queryset
