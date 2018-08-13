from django.core.management.base import BaseCommand, CommandError
from mturk_manager.models import Global_DB

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('token_instance', help='Instance token', type=str)
        parser.add_argument('token_worker', help='Worker token', type=str)

    def handle(self, *args, **options):
        Global_DB.objects.create(
            name='webis',
            token_instance=options['token_instance'],
            token_worker=options['token_worker'],
        )

        self.stdout.write(self.style.SUCCESS('Successfully set credentials for global DB "webis"'))
