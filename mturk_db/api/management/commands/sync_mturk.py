from django.core.management.base import BaseCommand

from api.classes import Manager_Projects, Manager_Batches


class Command(BaseCommand):
    help = 'Sync with MTurk'

    def add_arguments(self, parser):
        parser.add_argument('use_sandbox', help='Use Sandbox', type=bool)

    def handle(self, *args, **options):
        use_sandbox = options['use_sandbox']

        for project in Manager_Projects.get_all():
            self.stdout.write(self.style.SUCCESS('Syncing project {}'.format(project.name)))
            Manager_Batches.sync_mturk(project, use_sandbox)
