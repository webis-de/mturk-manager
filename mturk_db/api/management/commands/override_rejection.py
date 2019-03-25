from django.core.management.base import BaseCommand

from api.classes import Manager_Projects


class Command(BaseCommand):
    help = 'Override Rejection'

    def handle(self, *args, **options):
        client = Manager_Projects.get_mturk_api(False)

        result = client.approve_assignment(
            AssignmentId='',
            OverrideRejection=True
        )

        self.stdout.write(self.style.SUCCESS(result))
