from rest_framework.views import APIView
from rest_framework.response import Response
from mturk_db.permissions import IsInstance, IsWorker, AllowOptionsAuthentication
from api.classes import Manager_Workers
from rest_framework.decorators import api_view, permission_classes
from api.helpers import add_database_object_project
from api.serializers import Serializer_Worker
from api.models import Worker as Model_Worker
from rest_framework import status
from django.http import Http404

PERMISSIONS_WORKER_ONLY = (AllowOptionsAuthentication, IsWorker,)
PERMISSIONS_INSTANCE_ONLY = (AllowOptionsAuthentication, IsInstance,)

class Workers(APIView):
    permission_classes = PERMISSIONS_INSTANCE_ONLY

    # @add_database_object_project
    # def get(self, request, slug_project, database_object_project, use_sandbox, format=None):
    #     status_block = Manager_Workers.get_status_block(database_object_project, use_sandbox)
    #     # dictionary_counters = Manager_Workers.get_counter(database_object_project, use_sandbox)

    #     return Response({
    #         'blocks': status_block,
    #         # 'counters': dictionary_counters,
    #     })

    @add_database_object_project
    def patch(self, request, slug_project, database_object_project, use_sandbox, format=None):
        queryset_workers = Manager_Workers.sync_workers_by_ids(database_object_project, request.data, use_sandbox)
        serializer = Serializer_Worker(queryset_workers, many=True)

        # serializer = Serializer_Batch(data=request.data)
        return Response(serializer.data)


class Worker(APIView):
    def get_object(self, id_worker):
        try:
            return Model_Worker.objects.get(id=id_worker)
        except Model_Worker.DoesNotExist:
            raise Http404

    @add_database_object_project
    def put(self, request, slug_project, database_object_project, use_sandbox, id_worker, format=None):
        worker = self.get_object(id_worker)
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
