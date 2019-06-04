from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.classes import Manager_Messages_Reject
from api.helpers import add_database_object_project, paginate_queryset
from api.serializers import Serializer_Message_Reject
from mturk_db.permissions import IsInstance, IsWorker, AllowOptionsAuthentication

PERMISSIONS_INSTANCE_ONLY = (AllowOptionsAuthentication, IsInstance,)
PERMISSIONS_WORKER_ONLY = (AllowOptionsAuthentication, IsWorker,)


class MessagesReject(APIView):
    permission_classes = PERMISSIONS_INSTANCE_ONLY

    def get(self, request):
        queryset = Manager_Messages_Reject.get_all(
            request=request,
        )

        queryset_paginated, count_items = paginate_queryset(queryset, request)

        serializer = Serializer_Message_Reject(
            queryset_paginated,
            many=True,
            context={'request': request}
        )

        return Response({
            'items_total': count_items,
            'data': serializer.data,
        })


class ProjectMessagesReject(APIView):
    permission_classes = PERMISSIONS_INSTANCE_ONLY

    @add_database_object_project
    def get(self, request, slug_project, use_sandbox, database_object_project):
        queryset = Manager_Messages_Reject.get_all(
            request=request,
            database_object_project=database_object_project,
        )

        queryset_paginated, count_items = paginate_queryset(queryset, request)

        serializer = Serializer_Message_Reject(queryset_paginated, many=True, context={'request': request})

        return Response({
            'items_total': count_items,
            'data': serializer.data,
        })

    @add_database_object_project
    def post(self, request, slug_project, database_object_project, use_sandbox):
        serializer = Serializer_Message_Reject(data=request.data)

        if serializer.is_valid():
            serializer.save(database_object_project=database_object_project, use_sandbox=use_sandbox)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectMessageReject(APIView):
    permission_classes = PERMISSIONS_INSTANCE_ONLY

    @add_database_object_project
    def delete(self, request, slug_project, database_object_project, id_message, use_sandbox):
        Manager_Messages_Reject.delete_from_project(
            id_message=id_message,
            database_object_project=database_object_project,
        )

        return Response(status=status.HTTP_204_NO_CONTENT)
