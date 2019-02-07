import json

from rest_framework.settings import api_settings

from api.classes.finances import Manager_Finances
from api.serializers import Serializer_Assignment
from mturk_db.permissions import IsInstance, AllowOptionsAuthentication
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.helpers import add_database_object_project
from api.classes import Manager_Assignments
from api.models import Assignment
from rest_framework.decorators import api_view, permission_classes
from mturk_db.settings import REST_FRAMEWORK
PERMISSIONS_INSTANCE_ONLY = (AllowOptionsAuthentication, IsInstance,)

@api_view(['GET'])
@permission_classes(PERMISSIONS_INSTANCE_ONLY)
@add_database_object_project
def get_balance(request, slug_project, database_object_project, use_sandbox, format=None):
    balance = Manager_Finances.get_balance(database_object_project=database_object_project, use_sandbox=use_sandbox)
    return Response(balance)

# @api_view(['PUT'])
# @permission_classes(PERMISSIONS_INSTANCE_ONLY)
# @add_database_object_project
# def sync_mturk(request, slug_project, database_object_project, value, use_sandbox, format=None):
#     dictionary_data = Manager_Batches.sync_mturk(database_object_project, value)
#     # dictionary_data = {}
#     # return Response(True)
#     return Response(dictionary_data)

# class Assignment(APIView):
#     def get_object(self, id_assignment):
#         try:
#             return Assignment.objects.get(id=id_assignment)
#         except Assignment.DoesNotExist:
#             raise Http404

# #     # def get(self, request, name, format=None):
# #     #     project = self.get_object(name)
# #     #     serializer = Serializer_Project(project, context={'request': request})
# #     #     return Response(serializer.data)

#     @add_database_object_project
#     def put(self, request, slug_project, database_object_project, id_assignment, use_sandbox, format=None):
#         assignment = self.get_object(id_assignment)
#         serializer = Serializer_Assignment(assignment, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, name, format=None):
    #     project = self.get_object(name)
    #     project.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['DELETE'])
# @permission_classes(PERMISSIONS_INSTANCE_ONLY)
# @add_database_object_project
# def clear_sandbox(request, slug_project, database_object_project, use_sandbox, format=None):
#     dictionary_data = Manager_Batches.clear_sandbox(database_object_project)
#     # dictionary_data = {}
#     # return Response(True)
#     return Response(dictionary_data)