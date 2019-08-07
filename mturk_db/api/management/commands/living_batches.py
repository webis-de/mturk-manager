from django.core.management.base import BaseCommand

from api.classes import Manager_Templates_Worker, Manager_Batches
from api.models import Template_Worker, Batch
from django.db.models import Sum


class Command(BaseCommand):
    help = 'Are there any running batches?'

    def handle(self, *args, **options):
        queryset = Batch.objects.filter(use_sandbox=False)
        queryset = Manager_Batches.annotate_assignments(queryset)
        queryset = queryset.filter(count_assignments_living_total__gt=0)

        count_batches = queryset.count()
        projects = queryset.values('project__name').annotate(Sum('count_assignments_living_total'))

        if count_batches > 0:
            self.stdout.write(self.style.SUCCESS('{} living batches in the projects {}'.format(
                queryset.count(),
                ', '.join([project['project__name'] for project in projects])
            )))
        else:
            self.stdout.write(self.style.SUCCESS('No living batches'))
