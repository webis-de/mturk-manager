from rest_framework.views import APIView
from rest_framework.response import Response
from mturk_db.permissions import IsInstance, IsWorker, AllowOptionsAuthentication
from api.classes import Manager_Projects
from rest_framework.decorators import api_view, permission_classes
from api.helpers import add_database_object_project

PERMISSIONS_WORKER_ONLY = (AllowOptionsAuthentication, IsWorker,)
PERMISSIONS_INSTANCE_ONLY = (AllowOptionsAuthentication, IsInstance,)


@api_view(['GET'])
@permission_classes(PERMISSIONS_INSTANCE_ONLY)
@add_database_object_project
def get_count_assignments_max_per_worker(request, slug_project, database_object_project, use_sandbox, format=None):
    dictionary_data = Manager_Projects.get_count_assignments_max_per_worker(database_object_project)
    # dictionary_data = {}
    # return Response(True)
    return Response(dictionary_data)

@api_view(['PUT'])
@permission_classes(PERMISSIONS_INSTANCE_ONLY)
@add_database_object_project
def set_count_assignments_max_per_worker(request, slug_project, database_object_project, value, use_sandbox, format=None):
    dictionary_data = Manager_Projects.set_count_assignments_max_per_worker(database_object_project, value)
    # dictionary_data = {}
    # return Response(True)
    return Response(dictionary_data)