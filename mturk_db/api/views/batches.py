import json

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from api.classes import Manager_Batches
from api.helpers import add_database_object_project, paginate_queryset
from api.serializers import Serializer_Batch
from mturk_db.permissions import IsInstance, AllowOptionsAuthentication
from mturk_db.settings import REST_FRAMEWORK

PERMISSIONS_INSTANCE_ONLY = (AllowOptionsAuthentication, IsInstance,)


class Batches(APIView):
    permission_classes = PERMISSIONS_INSTANCE_ONLY

    @add_database_object_project
    def get(self, request, slug_project, database_object_project, use_sandbox, format=None):
        queryset = Manager_Batches.get_all(
            database_object_project=database_object_project,
            use_sandbox=use_sandbox,
            request=request
        )

        queryset_paginated, count_items = paginate_queryset(queryset, request)

        serializer = Serializer_Batch(
            queryset_paginated,
            many=True,
            context={
                'usecase': 'list_batches',
            }
        )

        return Response({
            'items_total': count_items,
            'data': serializer.data,
        })

    @add_database_object_project
    def post(self, request, slug_project, database_object_project, use_sandbox, format=None):
        serializer = Serializer_Batch(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save(database_object_project=database_object_project, use_sandbox=use_sandbox)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @add_database_object_project
    def patch(self, request, slug_project, database_object_project, use_sandbox, format=None):
        result = Manager_Batches.sync_mturk(database_object_project, use_sandbox)
        # list_batches_changed = Manager_Batches.sync_mturk(database_object_project, use_sandbox)
        # serializer = Serializer_Batch(list_batches_changed, many=True)

        return Response(result)


class Batch(APIView):
    @add_database_object_project
    def get(self, request, slug_project, database_object_project, use_sandbox, id_batch, format=None):
        batch = Manager_Batches.get(id_batch=id_batch)
        serializer = Serializer_Batch(
            batch,
            context={
                'detailed': True
            }
        )

        return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes(PERMISSIONS_INSTANCE_ONLY)
@add_database_object_project
def clear_sandbox(request, slug_project, database_object_project, use_sandbox, format=None):
    dictionary_data = Manager_Batches.clear_sandbox(database_object_project)

    return Response(dictionary_data)


@api_view(['GET'])
@permission_classes(PERMISSIONS_INSTANCE_ONLY)
@add_database_object_project
def batches_for_annotation(request, slug_project, database_object_project, use_sandbox, format=None):
    queryset = Manager_Batches.get_all(
        database_object_project=database_object_project,
        use_sandbox=use_sandbox,
        request=request
    )

    serializer = Serializer_Batch(
        queryset,
        context={
            'usecase': 'annotation',
        },
        many=True
    )

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes(PERMISSIONS_INSTANCE_ONLY)
@add_database_object_project
def download_batches(request, slug_project, database_object_project, use_sandbox, format=None):
    response = Manager_Batches.download(database_object_project, request)

    return response


@api_view(['GET'])
@permission_classes(PERMISSIONS_INSTANCE_ONLY)
@add_database_object_project
def download_info_batches(request, slug_project, database_object_project, use_sandbox, format=None):
    dictionary_data = Manager_Batches.download_info(database_object_project, request)

    return Response(dictionary_data)
