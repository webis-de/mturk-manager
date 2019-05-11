from django.db.models import Model, QuerySet, Count
from rest_framework.request import Request

from api.classes import Interface_Manager_Items
from api.helpers import raise_not_implemented_exception
from api.models import Project


class ManagerMessages(Interface_Manager_Items):
    model = None

    @classmethod
    def get_all(cls, database_object_project: Project, request: Request, fields: list = None) -> QuerySet:
        queryset = cls.model.objects.filter(
            project=database_object_project,
        )

        queryset = cls.annotate(
            queryset=queryset,
        )

        queryset = cls.sort_by(
            queryset=queryset,
            request=request,
        )

        if fields is not None:
            queryset = queryset.values(
                *fields
            )

        return queryset

    @staticmethod
    def annotate(queryset: QuerySet) -> QuerySet:
        return queryset.annotate(
            count_usage=Count('project', distinct=True),
        )

    @classmethod
    def get(cls, id_item: object) -> object:
        item = cls.model.objects.get(
            pk=id_item
        )

        return item

    @classmethod
    def create(cls, data: object) -> object:
        raise_not_implemented_exception('create', __class__)
        # instance = cls.model.objects.create(
        #     project = data['database_object_project'],
        #     name=data['name'],
        #     template=data['template'],
        # )
        #
        # return instance

    @classmethod
    def update(cls, instance: Model, data: dict) -> Model:
        for key, value in data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

    @classmethod
    def delete(cls, id_item: int) -> None:
        cls.model.objects.filter(id=id_item).delete()
