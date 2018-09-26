from api.models import Keyword
from mturk_db.settings import URL_MTURK_SANDBOX
import boto3, re, json
from django.utils.text import slugify
from collections import Counter
from django.conf import settings

class Manager_Keywords(object):
    @classmethod
    def get_all(cls):
        return Keyword.objects.all()