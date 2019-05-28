from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.db import IntegrityError

class Command(BaseCommand):
    help = 'Set the authentication tokens'

    def add_arguments(self, parser):
        parser.add_argument('token_instance', help='This token authenticates a client instance with the api', type=str)
        parser.add_argument('token_worker', help='This token authenticates the MTurk workers with the api', type=str)

    def handle(self, *args, **options):
        Token.objects.all().delete()

        try:
            object_instance = User.objects.create_user('instance')
            object_worker = User.objects.create_user('worker')
        except IntegrityError:
            object_instance = User.objects.get(username='instance')
            object_worker = User.objects.get(username='worker')

        Token.objects.create(
            key=options['token_instance'],
            user_id=object_instance.id,
        )

        Token.objects.create(
            key=options['token_worker'],
            user_id=object_worker.id,
        )

        self.stdout.write(self.style.SUCCESS('Successfully set authentication tokens'))
