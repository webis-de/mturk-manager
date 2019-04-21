from django.core.management.base import BaseCommand

from api.classes import Manager_Projects


class Command(BaseCommand):
    help = 'Override Rejection'

    def add_arguments(self, parser):
        parser.add_argument(
            'assignments',
            nargs='+',
            help='List of assignments',
            type=str
        )

    def handle(self, *args, **options):
        client = Manager_Projects.get_mturk_api(False)

        for assignment in options['assignments']:
            result = client.approve_assignment(
                AssignmentId=assignment,
                OverrideRejection=True
            )

            self.stdout.write(self.style.SUCCESS(result))
