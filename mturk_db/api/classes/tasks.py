from django.db.models import QuerySet, Model
from rest_framework.request import Request
from api.models import Project, CeleryTasks

from api.classes import Interface_Manager_Items


class ManagerTasks(Interface_Manager_Items):

    @classmethod
    def get_all(cls, request: Request, database_object_project: Project = None, fields: list = None) -> QuerySet:
        if database_object_project is None:
            queryset = CeleryTasks.objects.all()
        else:
            queryset = CeleryTasks.objects.filter(
                project=database_object_project
            )

        return queryset

    @staticmethod
    def create(data: dict) -> None:
        CeleryTasks.objects.create(
            project=data['database_object_project'],
            task=data['id'],
            description=data['description'],
            status=data['status'],
            datetime_created=data['datetime_created']
        )

    @staticmethod
    def delete(id_task: int) -> None:
        CeleryTasks.objects.filter(task=id_task).delete()
