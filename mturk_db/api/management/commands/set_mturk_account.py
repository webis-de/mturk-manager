from django.core.management.base import BaseCommand, CommandError
from api.models import Account_Mturk

class Command(BaseCommand):
    help = 'Create MTurk Accounts'

    def add_arguments(self, parser):
        parser.add_argument('name', help='Arbitrary name to distinguish this account', type=str)
        parser.add_argument('access_key', help='Access key', type=str)
        parser.add_argument('secret_key', help='Secret key', type=str)

    def handle(self, *args, **options):
        Account_Mturk.objects.all().delete()

        Account_Mturk.objects.create(
            name=options['name'].lower(),
            key_access=options['access_key'],
            key_secret=options['secret_key'],
        )

        self.stdout.write(self.style.SUCCESS('Successfully added mturk account "{}"'.format(options['name'])))
