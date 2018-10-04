# from mturk_manager.models import m_Project
from api.serializers import Serializer_Batch
from mturk_db.permissions import IsInstance, AllowOptionsAuthentication
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.helpers import add_database_object_project
from api.classes import Manager_Batches

PERMISSIONS_INSTANCE_ONLY = (AllowOptionsAuthentication, IsInstance,)

class Batches(APIView):
    permission_classes = PERMISSIONS_INSTANCE_ONLY

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
        print(serializer)
        if serializer.is_valid():
            serializer.save(database_object_project=database_object_project, use_sandbox=use_sandbox)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @add_database_object_project
    def patch(self, request, slug_project, database_object_project, use_sandbox, format=None):
        Manager_Batches.sync_mturk(database_object_project, use_sandbox)
        # serializer = Serializer_Batch(data=request.data)
        return Response({})

# @api_view(['PUT'])
# @permission_classes(PERMISSIONS_INSTANCE_ONLY)
# @add_database_object_project
# def sync_mturk(request, slug_project, database_object_project, value, use_sandbox, format=None):
#     dictionary_data = Manager_Batches.sync_mturk(database_object_project, value)
#     # dictionary_data = {}
#     # return Response(True)
#     return Response(dictionary_data)

# class Batch(APIView):
#     def get_object(self, slug):
#         try:
#             return m_Project.objects.get(slug=slug)
#         except m_Project.DoesNotExist:
#             raise Http404

#     # def get(self, request, name, format=None):
#     #     project = self.get_object(name)
#     #     serializer = Serializer_Project(project, context={'request': request})
#     #     return Response(serializer.data)

#     @add_database_object_project
#     def put(self, request, slug_project, database_object_project, use_sandbox, format=None):
#         # print('####')
#         # print(request.data)
#         # project = self.get_object(slug_project)
#         # serializer = Serializer_Project(project, data=request.data, partial=True)
#         # if serializer.is_valid():
#         #     serializer.save()
#         #     return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, name, format=None):
    #     project = self.get_object(name)
    #     project.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)