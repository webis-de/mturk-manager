from django.core.management.base import BaseCommand, CommandError
from api.models import Account_Mturk

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('access_key', help='Access key', type=str)
        parser.add_argument('secret_key', help='Secret key', type=str)

    def handle(self, *args, **options):
        Account_Mturk.objects.create(
            name='webis',
            key_access=options['access_key'],
            key_secret=options['secret_key'],
        )

        self.stdout.write(self.style.SUCCESS('Successfully set mturk account "webis"'))
