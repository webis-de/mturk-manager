from rest_framework.views import APIView
from rest_framework.response import Response
from mturk_db.permissions import IsInstance, IsWorker, AllowOptionsAuthentication
from api.classes import Manager_Keywords
from rest_framework.decorators import api_view, permission_classes
from api.helpers import add_database_object_project
from api.serializers import Serializer_Keyword
from rest_framework import status

PERMISSIONS_INSTANCE_ONLY = (AllowOptionsAuthentication, IsInstance,)
PERMISSIONS_WORKER_ONLY = (AllowOptionsAuthentication, IsWorker,)

class Keywords(APIView):
    permission_classes = PERMISSIONS_INSTANCE_ONLY

    def get(self, request, format=None):
        queryset_keywords = Manager_Keywords.get_all()
        serializer = Serializer_Keyword(queryset_keywords, many=True, context={'request': request})
        return Response(serializer.data)

    # @add_database_object_project
    # def post(self, request, slug_project, database_object_project, use_sandbox, format=None):
    #     serializer = Serializer_Settings_Batch(data=request.data)

    #     if serializer.is_valid():
    #         serializer.save(database_object_project=database_object_project)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class Setting_Batch(APIView):
#     permission_classes = PERMISSIONS_INSTANCE_ONLY

#     def get_object(self, id_settings_batch):
#         try:
#             return Model_Settings_Batch.objects.get(id=id_settings_batch)
#         except Model_Settings_Batch.DoesNotExist:
#             raise Http404

# #     # def get(self, request, name, format=None):
# #     #     project = self.get_object(name)
# #     #     serializer = Serializer_Settings_Batch(project, context={'request': request})
# #     #     return Response(serializer.data)

#     @add_database_object_project
#     def put(self, request, slug_project, database_object_project, use_sandbox, id_settings_batch, format=None):
#         project = self.get_object(id_settings_batch)
#         serializer = Serializer_Settings_Batch(project, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     @add_database_object_project
#     def delete(self, request, slug_project, database_object_project, use_sandbox, id_settings_batch, format=None):
#         Manager_Settings_Batch.delete(id_settings_batch)
#         return Response(status=status.HTTP_204_NO_CONTENT)
