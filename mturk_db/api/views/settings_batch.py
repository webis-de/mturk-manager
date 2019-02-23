from api.models import Settings_Batch as foo
from rest_framework.views import APIView
from rest_framework.response import Response
from mturk_db.permissions import IsInstance, IsWorker, AllowOptionsAuthentication
from api.classes import Manager_Settings_Batch
from rest_framework.decorators import api_view, permission_classes
from api.helpers import add_database_object_project
from api.serializers import Serializer_Settings_Batch
from api.models import Settings_Batch as Model_Settings_Batch
from rest_framework import status
from django.http import Http404
from mturk_db.settings import REST_FRAMEWORK
from rest_framework.settings import api_settings

PERMISSIONS_INSTANCE_ONLY = (AllowOptionsAuthentication, IsInstance,)
PERMISSIONS_WORKER_ONLY = (AllowOptionsAuthentication, IsWorker,)

class Settings_Batch(APIView):
    permission_classes = PERMISSIONS_INSTANCE_ONLY

    @add_database_object_project
    def get(self, request, slug_project, database_object_project, use_sandbox, format=None):

        queryset = Manager_Settings_Batch.get_page(database_object_project, request)

        queryset_paginated = queryset

        if request.query_params.get(REST_FRAMEWORK['PAGE_SIZE_QUERY_PARAM']) is not None:
            paginator = api_settings.DEFAULT_PAGINATION_CLASS()
            queryset_paginated = paginator.paginate_queryset(queryset, request)

        serializer = Serializer_Settings_Batch(queryset_paginated, many=True)

        return Response({
            'items_total': queryset.count(),
            'data': serializer.data,
        })


        queryset_settings_batch = Manager_Settings_Batch.get_all_for_project(database_object_project.id)
        serializer = Serializer_Settings_Batch(queryset_settings_batch, many=True, context={'request': request})
        return Response(serializer.data)

    @add_database_object_project
    def post(self, request, slug_project, database_object_project, use_sandbox, format=None):
        serializer = Serializer_Settings_Batch(data=request.data)

        if serializer.is_valid():
            serializer.save(database_object_project=database_object_project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Setting_Batch(APIView):
    permission_classes = PERMISSIONS_INSTANCE_ONLY

    def get(self, request, slug_project, id_settings_batch):
        item = Manager_Settings_Batch.get(id_settings_batch)
        serializer = Serializer_Settings_Batch(item, context={'request': request})
        return Response(serializer.data)

    @add_database_object_project
    def put(self, request, slug_project, database_object_project, use_sandbox, id_settings_batch, format=None):
        item = Manager_Settings_Batch.get(id_settings_batch)
        serializer = Serializer_Settings_Batch(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @add_database_object_project
    def delete(self, request, slug_project, database_object_project, use_sandbox, id_settings_batch, format=None):
        Manager_Settings_Batch.delete(id_settings_batch)
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes(PERMISSIONS_INSTANCE_ONLY)
@add_database_object_project
def settings_batch_all(request, slug_project, database_object_project, use_sandbox, format=None):
    list_fields = request.query_params.getlist('fields[]')
    if len(list_fields) == 0:
        list_fields = None

    queryset = Manager_Settings_Batch.get_all(
        database_object_project=database_object_project,
        fields=list_fields,
    )

    serializer = Serializer_Settings_Batch(queryset, many=True, context={
        'fields': list_fields,
    })

    return Response(serializer.data)