from mturk_manager.models import m_Project
from mturk.settings import URL_MTURK_SANDBOX
import boto3

class Manager_Projects(object):
    def __init__(self, arg):
        pass

    @staticmethod
    def get_mturk_api(database_object_project, use_sandbox=True):
        if use_sandbox:
            return boto3.client('mturk',
                aws_access_key_id=database_object_project.fk_account_mturk.key_access,
                aws_secret_access_key=database_object_project.fk_account_mturk.key_secret,
                region_name='us-east-1',
                endpoint_url=URL_MTURK_SANDBOX
            )
        else:
            return boto3.client('mturk',
                aws_access_key_id=database_object_project.fk_account_mturk.key_access,
                aws_secret_access_key=database_object_project.fk_account_mturk.key_secret,
                region_name='us-east-1'
            )