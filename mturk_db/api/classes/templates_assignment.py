from api.models import Account_Mturk, Template_Assignment
from mturk_db.settings import URL_MTURK_SANDBOX
import boto3, re, json
from django.utils.text import slugify
from collections import Counter
from django.conf import settings

class Manager_Templates_Assignment(object):
    @classmethod
    def get_all_for_project(cls, id_project):
        return Template_Assignment.objects.filter(project=id_project)

    @classmethod
    def create(cls, data):
        template_assignment = Template_Assignment.objects.create(
            project = data['database_object_project'],
            name=data['name'],
            template=data['template'],
        )

        return template_assignment
        
    @classmethod
    def update(cls, instance, data):
        for key, value in data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

    @staticmethod
    def delete(id_template):
        Template_Assignment.objects.filter(id=id_template).delete()

