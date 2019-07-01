from django.apps import AppConfig
from django.db.backends.signals import connection_created
import logging
from django.db import OperationalError

def new_connection(**kwargs):
    from api.models import Account_Mturk
    from django.contrib.auth.models import User

    try:
        if Account_Mturk.objects.count() == 0:
            logger = logging.getLogger(__name__)
            logger.critical('######################################################################################')
            logger.critical('# You did not add an MTurk account. Execute \'python3 manage.py set_mturk_account -h\' #')
            logger.critical('######################################################################################')

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
    except OperationalError:
        logger = logging.getLogger(__name__)
        logger.critical('######################################################################################')
        logger.critical('# Execute \'python3 manage.py migrate\' to initialize the database #')
        logger.critical('######################################################################################')


class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        connection_created.connect(new_connection)
