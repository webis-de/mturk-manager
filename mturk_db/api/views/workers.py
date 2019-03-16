from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from api.classes import Manager_Workers
from api.helpers import add_database_object_project
from api.serializers import Serializer_Worker
from mturk_db.permissions import IsInstance, IsWorker, AllowOptionsAuthentication
from mturk_db.settings import REST_FRAMEWORK

PERMISSIONS_WORKER_ONLY = (AllowOptionsAuthentication, IsWorker,)
PERMISSIONS_INSTANCE_ONLY = (AllowOptionsAuthentication, IsInstance,)

class Workers(APIView):
    permission_classes = PERMISSIONS_INSTANCE_ONLY

    @add_database_object_project
    def get(self, request, slug_project, database_object_project, use_sandbox, format=None):
        queryset = Manager_Workers.get_all(
            database_object_project=database_object_project,
            use_sandbox=use_sandbox,
            request=request
        )

        queryset_paginated = queryset

        if request.query_params.get(REST_FRAMEWORK['PAGE_SIZE_QUERY_PARAM']) is not None:
            paginator = api_settings.DEFAULT_PAGINATION_CLASS()
            queryset_paginated = paginator.paginate_queryset(queryset, request)

        serializer = Serializer_Worker(
            queryset_paginated,
            many=True
        )

        return Response({
            'items_total': queryset.count(),
            'data': serializer.data,
        })

    @add_database_object_project
    def patch(self, request, slug_project, database_object_project, use_sandbox, format=None):
        queryset_workers = Manager_Workers.sync_workers_by_ids(database_object_project, request.data, use_sandbox)
        serializer = Serializer_Worker(queryset_workers, many=True)

        # serializer = Serializer_Batch(data=request.data)
        return Response(serializer.data)


class Worker(APIView):

    @add_database_object_project
    def put(self, request, slug_project, database_object_project, use_sandbox, id_worker, format=None):
        worker = Manager_Workers.get(id_worker)
        serializer = Serializer_Worker(worker, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(database_object_project=database_object_project, use_sandbox=use_sandbox)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes(PERMISSIONS_INSTANCE_ONLY)
@add_database_object_project
def get_blocks_hard(request, slug_project, database_object_project, use_sandbox, format=None):
    dictionary_data = Manager_Workers.get_blocks_hard(database_object_project, request.data, use_sandbox)
    return Response(dictionary_data)

@api_view(['POST'])
@permission_classes(PERMISSIONS_INSTANCE_ONLY)
@add_database_object_project
def add_block_soft_for_worker(request, slug_project, database_object_project, id_worker, use_sandbox, format=None):
    dictionary_data = Manager_Workers.add_block_soft_for_worker(id_worker, database_object_project, use_sandbox)
    return Response(dictionary_data)

@api_view(['DELETE'])
@permission_classes(PERMISSIONS_INSTANCE_ONLY)
@add_database_object_project
def remove_block_soft_for_worker(request, slug_project, database_object_project, id_worker, use_sandbox, format=None):
    dictionary_data = Manager_Workers.remove_block_soft_for_worker(id_worker, database_object_project, use_sandbox)
    return Response(dictionary_data)

# @api_view(['PUT'])
# @permission_classes(PERMISSIONS_INSTANCE_ONLY)
# @add_database_object_project
# def set_count_assignments(request, slug_project, database_object_project, id_worker, use_sandbox, format=None):
#     dictionary_data = Manager_Workers.set_count_assignments(database_object_project, id_worker, request.data['count'])
#     return Response(dictionary_data)



@api_view(['GET'])
@permission_classes(PERMISSIONS_WORKER_ONLY)
@add_database_object_project
def status_block_for_worker(request, slug_project, database_object_project, id_worker, use_sandbox, format=None):
    dictionary_data = Manager_Workers.get_status_block_for_worker(database_object_project, id_worker)
    return Response(dictionary_data)

@api_view(['POST'])
@permission_classes(PERMISSIONS_WORKER_ONLY)
@add_database_object_project
def increment_counter_for_worker(request, slug_project, database_object_project, use_sandbox, format=None):
    dictionary_data = Manager_Workers.increment_counter_for_worker(database_object_project, request.data)
    return Response({})
