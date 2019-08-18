from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.db import IntegrityError
from django.conf import settings


class Command(BaseCommand):
    help = 'Setup'

    def handle(self, *args, **options):
        Token.objects.all().delete()

        try:
            object_instance = User.objects.create_user('instance')
            object_worker = User.objects.create_user('worker')
        except IntegrityError:
            object_instance = User.objects.get(username='instance')
            object_worker = User.objects.get(username='worker')

        Token.objects.create(
            key=settings.TOKEN_INSTANCE,
            user_id=object_instance.id,
        )

        Token.objects.create(
            key=settings.TOKEN_WORKER,
            user_id=object_worker.id,
        )

        self.stdout.write(self.style.SUCCESS('Successfully setup database'))
