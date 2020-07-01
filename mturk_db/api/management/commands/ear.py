import json

import boto3
from django.core.management.base import BaseCommand

from api.classes import Manager_Projects, Manager_Batches
from api.models import HIT
from django.core.serializers.json import DjangoJSONEncoder


class Command(BaseCommand):
    help = 'Exectue an API request'

    def handle(self, *args, **options):
        client = boto3.client('mturk',
             aws_access_key_id='***REMOVED***',
             aws_secret_access_key='***REMOVED***',
             region_name='us-east-1'
         )

        response = client.get_assignment(AssignmentId='3LRLIPTPEQ9EUCTISBCOJ5Q2JW4AKK')
        # response = client.get_hit(HITId='3KA7IJSNW65I1TXWLFCQMD0H62LPB4')

        print(json.dumps(response, cls=DjangoJSONEncoder))