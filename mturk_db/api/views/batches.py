from django.http import HttpResponse
from rest_framework.settings import api_settings

from api.serializers import Serializer_Batch
from mturk_db.permissions import IsInstance, AllowOptionsAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.helpers import add_database_object_project
from api.classes import Manager_Batches
from rest_framework.decorators import api_view, permission_classes
from api.models import Batch as Model_Batch
import json

from mturk_db.settings import REST_FRAMEWORK

PERMISSIONS_INSTANCE_ONLY = (AllowOptionsAuthentication, IsInstance,)

class Batches(APIView):
    permission_classes = PERMISSIONS_INSTANCE_ONLY

    @add_database_object_project
    def get(self, request, slug_project, database_object_project, use_sandbox, format=None):
        queryset = Manager_Batches.get(database_object_project, use_sandbox, request)

        queryset_paginated = queryset

        if request.query_params.get(REST_FRAMEWORK['PAGE_SIZE_QUERY_PARAM']) is not None:
            paginator = api_settings.DEFAULT_PAGINATION_CLASS()
            queryset_paginated = paginator.paginate_queryset(queryset, request)

        serializer = Serializer_Batch(queryset_paginated, many=True)

        return Response({
            'items_total': queryset.count(),
            'data': serializer.data,
        })

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
        list_batches_changed = Manager_Batches.sync_mturk(database_object_project, use_sandbox)
        serializer = Serializer_Batch(list_batches_changed, many=True)

        # serializer = Serializer_Batch(data=request.data)
        return Response(serializer.data)

# @api_view(['PUT'])
# @permission_classes(PERMISSIONS_INSTANCE_ONLY)
# @add_database_object_project
# def sync_mturk(request, slug_project, database_object_project, value, use_sandbox, format=None):
#     dictionary_data = Manager_Batches.sync_mturk(database_object_project, value)
#     # dictionary_data = {}
#     # return Response(True)
#     return Response(dictionary_data)

class Batch(APIView):
    def get_object(self, id_batch):
        try:
            return Model_Batch.objects.get(pk=id_batch)
        except Model_Batch.DoesNotExist:
            raise Http404

    @add_database_object_project
    def get(self, request, slug_project, database_object_project, use_sandbox, id_batch, format=None):
        batch = Manager_Batches.get_by_id(id_batch=id_batch)
        serializer = Serializer_Batch(
            batch,
            context={
                'detailed': True
            }
        )
        # serializer = Serializer_Project(database_object_project, context={'request': request})
        return Response(serializer.data)

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

@api_view(['DELETE'])
@permission_classes(PERMISSIONS_INSTANCE_ONLY)
@add_database_object_project
def clear_sandbox(request, slug_project, database_object_project, use_sandbox, format=None):
    dictionary_data = Manager_Batches.clear_sandbox(database_object_project)
    # dictionary_data = {}
    # return Response(True)
    return Response(dictionary_data)

@api_view(['GET'])
@permission_classes(PERMISSIONS_INSTANCE_ONLY)
@add_database_object_project
def batches_for_annotation(request, slug_project, database_object_project, use_sandbox, format=None):
    list_ids = json.loads(request.query_params.get('list_ids', '[]'))
    queryset_batches = Model_Batch.objects.filter(id__in=list_ids)
    # queryset_batches = Manager_Batches.batches_for_annotation(database_object_project, list_ids)
    serializer = Serializer_Batch(
        queryset_batches, 
        context={
            'detailed': True
        }, 
        many=True
    )
    return Response(serializer.data)
    # return Response(dictionary_data)

@api_view(['GET'])
@permission_classes(PERMISSIONS_INSTANCE_ONLY)
@add_database_object_project
def download_batches(request, slug_project, database_object_project, use_sandbox, format=None):
    response = Manager_Batches.download(database_object_project, request)

    return response

@api_view(['GET'])
@permission_classes(PERMISSIONS_INSTANCE_ONLY)
@add_database_object_project
def download_info_batches(request, slug_project, database_object_project, use_sandbox, format=None):
    dictionary_data = Manager_Batches.download_info(database_object_project, request)

    return Response(dictionary_data)
