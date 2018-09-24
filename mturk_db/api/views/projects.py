from rest_framework.views import APIView
from rest_framework.response import Response
from mturk_db.permissions import IsInstance, IsWorker, AllowOptionsAuthentication
from api.classes import Manager_Projects
from rest_framework.decorators import api_view, permission_classes
from api.helpers import add_database_object_project
from api.serializers import Serializer_Project
from rest_framework import status

PERMISSIONS_INSTANCE_ONLY = (AllowOptionsAuthentication, IsInstance,)
PERMISSIONS_WORKER_ONLY = (AllowOptionsAuthentication, IsWorker,)

class Projects(APIView):
    permission_classes = PERMISSIONS_INSTANCE_ONLY

    # @add_database_object_project
    def get(self, request, format=None):
        queryset_projects = Manager_Projects.get_all()
        serializer = Serializer_Project(queryset_projects, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = Serializer_Project(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Project(APIView):
    permission_classes = PERMISSIONS_INSTANCE_ONLY

    def get_object(self, slug):
        try:
            return m_Project.objects.get(slug=slug)
        except m_Project.DoesNotExist:
            raise Http404

    # def get(self, request, name, format=None):
    #     project = self.get_object(name)
    #     serializer = Serializer_Project(project, context={'request': request})
    #     return Response(serializer.data)

    @add_database_object_project
    def put(self, request, slug_project, database_object_project, use_sandbox, format=None):
        print('####')
        print(request.data)
        project = self.get_object(slug_project)
        serializer = Serializer_Project(project, data=request.data, partial=True)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, name, format=None):
    #     project = self.get_object(name)
    #     project.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes(PERMISSIONS_INSTANCE_ONLY)
# @add_database_object_project
def projects_check_uniqueness(request, name_project, format=None):
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