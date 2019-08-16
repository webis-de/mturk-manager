from rest_framework.views import APIView
from rest_framework.response import Response
from mturk_db.permissions import IsInstance, IsWorker, AllowOptionsAuthentication
from api.classes import Manager_Projects
from rest_framework.decorators import api_view, permission_classes
from api.helpers import add_database_object_project
from api.serializers import Serializer_Project
from api.models import Project as Model_Project
from rest_framework import status
from django.http import Http404
from api.helpers import migrate_project

PERMISSIONS_INSTANCE_ONLY = (AllowOptionsAuthentication, IsInstance,)
PERMISSIONS_WORKER_ONLY = (AllowOptionsAuthentication, IsWorker,)

class Projects(APIView):
    permission_classes = PERMISSIONS_INSTANCE_ONLY

    # @add_database_object_project
    def get(self, request, format=None):
        # list_projects = [
        #     # 'real-money-web-page-segmentation-01',
        #     # 'real-money-web-page-segmentation-02',
        #     # 'real-money-web-page-segmentation-02-rest',
        #     # 'real-money-web-page-segmentation-03',
        # ]
        #
        # for name_project in list_projects:
        #     migrate_project(name_project)

        queryset_projects = Manager_Projects.get_all()

        serializer = Serializer_Project(
            queryset_projects,
            many=True,
            context={
                'request': request,
            })
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = Serializer_Project(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Project(APIView):
    permission_classes = PERMISSIONS_INSTANCE_ONLY

    @add_database_object_project
    def get(self, request, slug_project, database_object_project, use_sandbox, format=None):
        project = Manager_Projects.get(database_object_project)
        serializer = Serializer_Project(
            project,
        )
        # serializer = Serializer_Project(database_object_project, context={'request': request})
        return Response(serializer.data)

    @add_database_object_project
    def put(self, request, slug_project, database_object_project, use_sandbox, format=None):
        serializer = Serializer_Project(database_object_project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @add_database_object_project
    def delete(self, request, slug_project, database_object_project, use_sandbox, format=None):
        Manager_Projects.delete(database_object_project)
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes(PERMISSIONS_INSTANCE_ONLY)
# @add_database_object_project
def projects_check_uniqueness(request, name_project):
    is_unique = Manager_Projects.check_uniqueness(name_project)
    # import time
    # time.sleep(1)
    return Response(is_unique)

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

@api_view(['PUT'])
@permission_classes(PERMISSIONS_INSTANCE_ONLY)
@add_database_object_project
def ping(request, slug_project, database_object_project, use_sandbox, format=None):
    dictionary_data = Manager_Projects.ping(database_object_project)
    return Response(dictionary_data)