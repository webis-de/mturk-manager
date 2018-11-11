from django.db.models import F, Value, Count, Q, Sum, IntegerField, ExpressionWrapper
from api.models import Account_Mturk, Project, Message_Reject
from mturk_db.settings import URL_MTURK_SANDBOX
import boto3
from pytz import timezone
from datetime import datetime
from django.utils.text import slugify
from django.conf import settings

class Manager_Projects(object):
    try:
        object_account_mturk = Account_Mturk.objects.all()[0]
        # object_account_mturk = Account_Mturk.objects.get(name='webis')
    except:
        raise Exception('No credentials for the MTurk account are set')

    @classmethod
    def get_all(cls):
        return Project.objects.all()

    @classmethod
    def get_mturk_api(cls, use_sandbox=True):
        if use_sandbox:
            return boto3.client('mturk',
                aws_access_key_id=cls.object_account_mturk.key_access,
                aws_secret_access_key=cls.object_account_mturk.key_secret,
                region_name='us-east-1',
                endpoint_url=URL_MTURK_SANDBOX
            )
        else:
            return boto3.client('mturk',
                aws_access_key_id=cls.object_account_mturk.key_access,
                aws_secret_access_key=cls.object_account_mturk.key_secret,
                region_name='us-east-1'
            )

    @classmethod
    def check_uniqueness(cls, name):
        return not Project.objects.filter(name=name).exists()

    @classmethod
    def create(cls, data):
        project = Project.objects.create(
            name=data['name'],
            slug=slugify(data['name']),
            fk_account_mturk=cls.object_account_mturk,
            version=settings.VERSION_PROJECT,
        )

        return project

    @staticmethod
    def update(instance, validated_data):
        for key, value in validated_data.items():
            if key == 'message_reject':
                message_reject = Message_Reject.objects.get_or_create(message=value)[0]
                instance.message_reject_default = message_reject

                messages_reject_deleted = Message_Reject.objects.all().annotate(
                    count_usage=Count('project')
                ).filter(count_usage=0).delete()
            else:
                setattr(instance, key, value)

        instance.save()
        return instance

    @classmethod
    def get_count_assignments_max_per_worker(cls, database_object_project):
        project = Project.objects.get(slug=database_object_project.slug)

        return {
            'count_assignments_max_per_worker': project.count_assignments_max_per_worker,
        }

    @classmethod
    def set_count_assignments_max_per_worker(cls, database_object_project, value):
        project = Project.objects.filter(slug=database_object_project.slug).update(
            count_assignments_max_per_worker=value
        )

        return {
            'count_assignments_max_per_worker': value,
        }

    @staticmethod
    def ping(database_object_project):
        now = datetime.now(timezone('Europe/Berlin'))
        database_object_project.datetime_visited = now
        database_object_project.save()
        return { 'datetime': now }

    @staticmethod
    def delete(database_object_project):
        database_object_project.delete()
