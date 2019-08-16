from django.apps import AppConfig
from django.db.backends.signals import connection_created
import logging
from django.db import OperationalError

def new_connection(**kwargs):
    from django.contrib.auth.models import User

    try:
        try:
            worker = User.objects.get(username='worker')
            instance = User.objects.get(username='instance')

            worker.auth_token
            instance.auth_token
        except Exception:
            logger = logging.getLogger(__name__)
            logger.critical('######################################################################################')
            logger.critical('# You did not set the authentication tokens. Execute \'python3 manage.py set_tokens -h\' #')
            logger.critical('######################################################################################')
    except Exception:
        logger = logging.getLogger(__name__)
        logger.critical('######################################################################################')
        logger.critical('# Execute \'python3 manage.py migrate\' to initialize the database (Ignore this message if you are currently migrating) #')
        logger.critical('######################################################################################')


class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        connection_created.connect(new_connection)
