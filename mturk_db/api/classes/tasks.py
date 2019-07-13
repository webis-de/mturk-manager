from django.db.models import QuerySet, Model, Case, When, TextField, F, Subquery, OuterRef
from rest_framework.request import Request

from api.enums import STATUS_TASK
from api.models import Project, CeleryTasks
from django.utils import timezone
from django_celery_results.models import TaskResult

from api.classes import Interface_Manager_Items


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
        print(TaskResult.objects.all())
        return queryset.annotate(
            payload=Case(
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
            datetime_created=data['datetime_created']
        )

    @staticmethod
    def delete(id_task: int) -> None:
        CeleryTasks.objects.filter(task=id_task).delete()

    @staticmethod
    def start(id_task: int) -> None:
        CeleryTasks.objects.filter(task=id_task).update(
            datetime_started=timezone.now(),
            status=STATUS_TASK.PROGRESS,
        )
