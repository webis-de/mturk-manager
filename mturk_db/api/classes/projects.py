from api.models import Account_Mturk
from mturk_db.settings import URL_MTURK_SANDBOX
import boto3

class Manager_Projects(object):
    object_account_mturk = Account_Mturk.objects.get(name='webis')

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