from django.db.models import Model, QuerySet, Count, Q
from rest_framework.request import Request

from api.classes import Interface_Manager_Items
from api.helpers import raise_not_implemented_exception
from api.models import Project
from api.models import Message


class ManagerMessages(Interface_Manager_Items):
    model = None

    @classmethod
    def get_all(cls, request: Request, database_object_project: Project = None, fields: list = None) -> QuerySet:
        if database_object_project is None:
            queryset = cls.model.objects.all()
        else:
            queryset = cls.model.objects.filter(
                Q(project=database_object_project) | Q(projects=database_object_project),
            )

        queryset = cls.filter(
            queryset=queryset,
            request=request
        )

        queryset = cls.annotate(
            queryset=queryset,
        )

        queryset = cls.sort_by(
            queryset=queryset,
            request=request,
        )

        queryset = cls.limit(
            queryset=queryset,
            request=request,
        )

        if fields is not None:
            queryset = queryset.values(
                *fields
            )

        return queryset

    @staticmethod
    def filter(queryset: QuerySet, request: Request) -> QuerySet:
        search = request.query_params.get('search')
        if search is not None:
            queryset = queryset.filter(
                message_lowercase__contains=search
            )

        return queryset

    @staticmethod
    def annotate(queryset: QuerySet) -> QuerySet:
        return queryset.annotate(
            count_usage=Count('project', distinct=True) + Count('projects', distinct=True),
        )

    @classmethod
    def get(cls, id_item: object) -> object:
        item = cls.model.objects.get(
            pk=id_item
        )

        return item

    @classmethod
    def create(cls, data: dict, database_object_project: Project = None) -> Message:
        print(data)
        print(database_object_project)

        message = data.get('message')
        if message is not None:
            instance, was_created = cls.model.objects.get_or_create(
                message=message,
                message_lowercase=message.lower(),
            )
        else:
            instance = cls.model.objects.get(id=data.get('id'))

        instance.projects.add(database_object_project)

        return instance

    @classmethod
    def update(cls, instance: Model, data: dict) -> Model:
        for key, value in data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

    @classmethod
    def delete(cls, id_item: int) -> None:
        cls.model.objects.filter(id=id_item).delete()

    @classmethod
    def delete_from_project(cls, id_message: int, database_object_project: Project) -> None:
        message = cls.model.objects.get(id=id_message)
        message.projects.remove(database_object_project)
        cls.delete_if_no_usage(message)

    @classmethod
    def delete_if_no_usage(cls, message: Message):
        cls.annotate(
            cls.model.objects.filter(id=message.id)
        ).filter(
            count_usage=0
        ).delete()
