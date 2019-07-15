from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from api.classes import ManagerTasks
from api.helpers import add_database_object_project, paginate_queryset
from api.serializers.serializer_task import SerializerTasks
from mturk_db.permissions import IsInstance, AllowOptionsAuthentication

PERMISSIONS_INSTANCE_ONLY = (AllowOptionsAuthentication, IsInstance,)


class Tasks(APIView):
    permission_classes = PERMISSIONS_INSTANCE_ONLY

    @add_database_object_project
    def get(self, request, slug_project, database_object_project, use_sandbox, format=None):
        queryset = ManagerTasks.get_all(
            database_object_project=database_object_project,
            request=request
        )

        queryset_paginated, count_items = paginate_queryset(queryset, request)

        serializer = SerializerTasks(
            queryset_paginated,
            many=True,
        )

        return Response({
            'items_total': count_items,
            'data': serializer.data,
        })


class Task(APIView):
    permission_classes = PERMISSIONS_INSTANCE_ONLY

    @add_database_object_project
    def delete(self, request, slug_project, database_object_project, use_sandbox, id_task, format=None):
        ManagerTasks.delete(id_task)
        return Response(status=status.HTTP_204_NO_CONTENT)
