from django.db.models import F, Value, Count, Q, Sum, IntegerField, ExpressionWrapper
from api.models import Message_Reject
# from mturk_db.settings import URL_MTURK_SANDBOX
import boto3, re, json
from django.utils.text import slugify
from collections import Counter
from django.conf import settings

class Manager_Messages_Reject(object):
    @classmethod
    def get_all(cls):
        return Message_Reject.objects.all().annotate(
            count_usage=Count('project', distinct=True)
        )