from api.models import Account_Mturk, Template_Worker
from mturk_db.settings import URL_MTURK_SANDBOX
import boto3, re, json
from django.utils.text import slugify
from collections import Counter
from django.conf import settings

class Manager_Templates_Worker(object):
    @classmethod
    def get_all_for_project(cls, id_project):
        return Template_Worker.objects.filter(project=id_project)

    @classmethod
    def create(cls, data):
        template_worker = Template_Worker.objects.create(
            project = data['database_object_project'],
            name=data['name'],
            height_frame=data['height_frame'],
            template=data['template'],
            json_dict_parameters=json.dumps(cls.count_parameters_in_template(data['template'])),
        )

        return template_worker

    @staticmethod
    def count_parameters_in_template(string_template):
        list_matches = re.findall('\$\{([a-zA-Z0-9_-]+)\}', string_template)
        counter = Counter(list_matches)
        return counter

    @staticmethod
    def delete(id_template):
        Template_Worker.objects.filter(id=id_template).delete()

