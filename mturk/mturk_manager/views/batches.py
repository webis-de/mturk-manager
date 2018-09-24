# from mturk_manager.models import m_Project
from mturk_manager.serializers import Serializer_Batch
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mturk_manager.helpers import add_database_object_project
from mturk_manager.classes import Manager_Batches

class Batches(APIView):
    @add_database_object_project
    def get(self, request, slug_project, database_object_project, use_sandbox, format=None):
        querset_batches = Manager_Batches.get_all(database_object_project, use_sandbox)
        # queryset_projects = m_Project.objects.all()
        # serializer = Serializer_Project(queryset_projects, many=True, context={'request': request})
        serializer = Serializer_Batch(querset_batches, many=True)
        return Response(serializer.data)

    @add_database_object_project
    def post(self, request, slug_project, database_object_project, use_sandbox, format=None):
        serializer = Serializer_Batch(data=request.data)
        if serializer.is_valid():
            serializer.save(database_object_project=database_object_project, use_sandbox=use_sandbox)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Batch(APIView):
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
        # print('####')
        # print(request.data)
        # project = self.get_object(slug_project)
        # serializer = Serializer_Project(project, data=request.data, partial=True)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, name, format=None):
    #     project = self.get_object(name)
    #     project.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)