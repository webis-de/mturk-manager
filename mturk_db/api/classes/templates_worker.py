import json
import re
from collections import Counter

from django.db.models import Model

from api.classes import Manager_Templates
from api.models import Template_Worker


class Manager_Templates_Worker(Manager_Templates):
    model = Template_Worker

    @classmethod
    def create(cls, data: dict) -> Template_Worker:
        template = Template_Worker.objects.create(
            project = data['database_object_project'],
            name=data['name'],
            height_frame=data['height_frame'],
            template=data['template'],
            json_dict_parameters=json.dumps(cls.count_parameters_in_template(data['template'])),
            template_assignment=data.get('template_assignment', None),
            template_hit=data.get('template_hit', None),
            template_global=data.get('template_global', None),
        )

        return template

    @staticmethod
    def count_parameters_in_template(string_template):
        list_matches = re.findall('\$\{([a-zA-Z0-9_-]+)\}', string_template)
        counter = Counter(list_matches)
        return counter

    @classmethod
    def update(cls, instance: Model, data: dict) -> Template_Worker:
        for key, value in data.items():
            if key == 'template':
                instance.json_dict_parameters = json.dumps(cls.count_parameters_in_template(value))
            setattr(instance, key, value)

        instance.save()

        return instance
