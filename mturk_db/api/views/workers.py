from rest_framework.views import APIView
from rest_framework.response import Response
from mturk_db.permissions import IsInstance, IsWorker, AllowOptionsAuthentication
from api.classes import Manager_Workers
from rest_framework.decorators import api_view, permission_classes
from api.helpers import add_database_object_project

PERMISSIONS_WORKER_ONLY = (AllowOptionsAuthentication, IsWorker,)
PERMISSIONS_INSTANCE_ONLY = (AllowOptionsAuthentication, IsInstance,)

class Workers(APIView):
    permission_classes = PERMISSIONS_INSTANCE_ONLY
    
    # def get_object(self, name):
    #     try:
    #         return m_Worker.objects.get(name=name)
    #     except m_Worker.DoesNotExist:
    #         raise Http404

    @add_database_object_project
    def get(self, request, slug_project, database_object_project, use_sandbox, format=None):
        status_block = Manager_Workers.get_status_block(database_object_project, use_sandbox)
        # print(request.user)
        print(use_sandbox)
        print(use_sandbox)
        print(use_sandbox)
        # print(request.auth)

    # def get(self, request, name, format=None):
        # worker = self.get_object(name)
        # serializer = Serializer_Worker(worker)
        return Response(status_block)

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
    # return Response(dictionary_data)
