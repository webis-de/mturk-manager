from django.core.management.base import BaseCommand

from api.classes import Manager_Templates_Worker
from api.models import Template_Worker, Batch


class Command(BaseCommand):
    help = 'Corrects worker templates'

    def handle(self, *args, **options):
        Batch.objects.select_related('settings_batch__template_worker').filter(project__isnull=True).delete()
        print('Templates: {}'.format(Template_Worker.objects.count()))
        for batch in Batch.objects.prefetch_related('settings_batch__template_worker').select_related('project', 'settings_batch__template_worker').all():
            Manager_Templates_Worker.clone_and_fix_template(batch.settings_batch.template_worker)
        print('Templates: {}'.format(Template_Worker.objects.count()))

        self.stdout.write(self.style.SUCCESS('Corrected worker templates'))
