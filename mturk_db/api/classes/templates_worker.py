import json
import re
from collections import Counter

from django.db.models import QuerySet, Case, When, BooleanField, Count, F
from django.db.models.functions import Coalesce
from rest_framework.request import Request
from django.utils import timezone

from api.classes import Manager_Templates
from api.models import Template_Worker


class Manager_Templates_Worker(Manager_Templates):
    model = Template_Worker

    @staticmethod
    def filter(queryset: QuerySet, request: Request) -> QuerySet:
        return queryset.filter(
            template_original=None
        )

    @staticmethod
    def annotate(queryset: QuerySet) -> QuerySet:
        return queryset.annotate(
            count_batches=Count('settings_batch')
        ).annotate(
            has_assignments=Case(
                When(count_batches__gt=0,
                     then=True
                 ),
                default=False,
                output_field=BooleanField()
            )
        )

    @classmethod
    def create(cls, data: dict) -> Template_Worker:
        template = Template_Worker.objects.create(
            project=data['database_object_project'],
            name=data['name'],
            height_frame=data['height_frame'],
            template=data['template'],
            json_dict_parameters=json.dumps(cls.count_parameters_in_template(data['template'])),
            template_assignment=data.get('template_assignment', None),
            template_hit=data.get('template_hit', None),
            template_global=data.get('template_global', None),
        )

        template_original = data.get('template_original', None)
        if template_original is not None:
            if template_original is True:
                template.template_original = template
            else:
                template.template_original = template_original

            template.save()

        template.has_assignments = False

        return template

    @staticmethod
    def count_parameters_in_template(string_template):
        list_matches = re.findall('\$\{([a-zA-Z0-9_-]+)\}', string_template)
        counter = Counter(list_matches)
        return counter

    @classmethod
    def update(cls, instance: Template_Worker, data: dict) -> Template_Worker:
        for key, value in data.items():
            if key == 'template':
                instance.json_dict_parameters = json.dumps(cls.count_parameters_in_template(value))
            setattr(instance, key, value)

        instance.save()

        return instance

    @classmethod
    def clone_and_fix_template(cls, template: Template_Worker):
        # create a copy of the worker template and fix it
        return Template_Worker.objects.create(
            name='{}__{}'.format(template.name, timezone.now().timestamp()),
            project=template.project,
            template=template.template,
            is_active=template.is_active,
            height_frame=template.height_frame,
            template_assignment=template.template_assignment,
            template_hit=template.template_hit,
            template_global=template.template_global,
            json_dict_parameters=template.json_dict_parameters,
            template_original=template,
        )
