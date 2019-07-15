import json

from django.db.models import QuerySet, Case, When, TextField, Subquery, OuterRef
from django.utils import timezone
from django_celery_results.models import TaskResult
from rest_framework.request import Request

from api.classes import Interface_Manager_Items
from api.enums import STATUS_TASK
from api.models import Project, CeleryTasks


class ManagerTasks(Interface_Manager_Items):

    @staticmethod
    def get_all(request: Request, database_object_project: Project = None, fields: list = None) -> QuerySet:
        if database_object_project is None:
            queryset = CeleryTasks.objects.all()
        else:
            queryset = CeleryTasks.objects.filter(
                project=database_object_project
            )

        queryset = ManagerTasks.annotate(queryset)

        return queryset

    @staticmethod
    def annotate(queryset: QuerySet) -> QuerySet:
        return queryset.annotate(
            payloadExtern=Case(
                When(
                    datetime_started__isnull=False,
                    then=Subquery(TaskResult.objects.filter(task_id=OuterRef('task')).values('result'))
                ),
                output_field=TextField(),
            ),
        )

    @staticmethod
    def create(data: dict) -> None:
        CeleryTasks.objects.create(
            project=data['database_object_project'],
            task=data['id'],
            description=data['description'],
            status=data['status'],
            datetime_created=data['datetime_created'],
            payload=json.dumps(data['payload'])
        )

    @staticmethod
    def delete(id_task: int) -> None:
        CeleryTasks.objects.filter(id=id_task).delete()

    @staticmethod
    def delete_by_uid(id_task: int) -> None:
        CeleryTasks.objects.filter(task=id_task).delete()

    @staticmethod
    def start(id_task: int) -> None:
        CeleryTasks.objects.filter(task=id_task).update(
            datetime_started=timezone.now(),
            status=STATUS_TASK.PROGRESS,
        )

    @staticmethod
    def failed(id_task: int) -> None:
        CeleryTasks.objects.filter(task=id_task).update(
            datetime_finished=timezone.now(),
            status=STATUS_TASK.FAILED,
        )
