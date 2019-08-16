from django.apps import AppConfig
from django.db.backends.signals import connection_created
import logging
from django.db import IntegrityError
from django.conf import settings

def new_connection(**kwargs):
    from django.contrib.auth.models import User
    from rest_framework.authtoken.models import Token

    # try:
    try:
        object_instance = User.objects.create_user('instance')
        object_worker = User.objects.create_user('worker')
    except IntegrityError:
        object_instance = User.objects.get(username='instance')
        object_worker = User.objects.get(username='worker')

    Token.objects.all().delete()

    Token.objects.create(
        key=settings.TOKEN_INSTANCE,
        user_id=object_instance.id,
    )

    Token.objects.create(
        key=settings.TOKEN_WORKER,
        user_id=object_worker.id,
    )

    # except Exception:
    #     logger = logging.getLogger(__name__)
    #     logger.critical('######################################################################################')
    #     logger.critical('# Execute \'python3 manage.py migrate\' to initialize the database (Ignore this message if you are currently migrating) #')
    #     logger.critical('######################################################################################')


class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        connection_created.connect(new_connection)
