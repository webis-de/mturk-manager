from api.models import Account_Mturk, Project
from mturk_db.settings import URL_MTURK_SANDBOX
import boto3
from django.utils.text import slugify
from django.conf import settings

class Manager_Projects(object):
    try:
        object_account_mturk = Account_Mturk.objects.get(name='webis')
    except:
        print('No credentials for the MTurk account are set')

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
