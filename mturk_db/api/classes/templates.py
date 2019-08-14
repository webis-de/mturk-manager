from django.db.models import Model, QuerySet
from rest_framework.request import Request

from api.classes import Interface_Manager_Items
from api.models import Project
from typing import Tuple


class Manager_Templates(Interface_Manager_Items):
    model = None

    @classmethod
    def get_all(cls, database_object_project: Project, request: Request) -> Tuple[QuerySet, list]:
        queryset = cls.model.objects.filter(
            project=database_object_project,
        )

        queryset = cls.filter(
            queryset=queryset,
            request=request,
        )

        queryset = cls.annotate(
            queryset=queryset,
        )

        queryset = cls.sort_by(
            queryset=queryset,
            request=request,
        )

        queryset, list_fields = cls.fields(
            queryset=queryset,
            request=request,
        )

        return queryset, list_fields

    @staticmethod
    def filter(queryset: QuerySet, request: Request) -> QuerySet:
        return queryset

    @staticmethod
    def annotate(queryset: QuerySet) -> QuerySet:
        return queryset

    @classmethod
    def get(cls, id_item: object) -> object:
        item = cls.model.objects.get(
            pk=id_item
        )

        return item

    @classmethod
    def create(cls, data: object) -> object:
        template = cls.model.objects.create(
            project = data['database_object_project'],
            name=data['name'],
            template=data['template'],
        )

        return template

    @classmethod
    def update(cls, instance: Model, data: dict) -> Model:
        for key, value in data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

    @classmethod
    def delete(cls, id_item: int) -> None:
        cls.model.objects.filter(id=id_item).delete()
