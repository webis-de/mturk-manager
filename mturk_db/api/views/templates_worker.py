from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from api.classes import Manager_Templates_Worker
from api.helpers import add_database_object_project
from api.serializers import Serializer_Template_Worker
from mturk_db.permissions import IsInstance, IsWorker, AllowOptionsAuthentication
from mturk_db.settings import REST_FRAMEWORK

PERMISSIONS_INSTANCE_ONLY = (AllowOptionsAuthentication, IsInstance,)
PERMISSIONS_WORKER_ONLY = (AllowOptionsAuthentication, IsWorker,)

class Templates_Worker(APIView):
    permission_classes = PERMISSIONS_INSTANCE_ONLY

    @add_database_object_project
    def get(self, request, slug_project, database_object_project, use_sandbox, format=None):
        queryset = Manager_Templates_Worker.get_all(
            database_object_project=database_object_project,
            request=request,
        )

        queryset_paginated = queryset

        if request.query_params.get(REST_FRAMEWORK['PAGE_SIZE_QUERY_PARAM']) is not None:
            paginator = api_settings.DEFAULT_PAGINATION_CLASS()
            queryset_paginated = paginator.paginate_queryset(queryset, request)
            count_items = paginator.page.paginator.count
        else:
            count_items = queryset.count()

        serializer = Serializer_Template_Worker(
            queryset_paginated,
            many=True,
            context={
                'request': request,
                'usecase': 'list_templates_worker',
            }
        )

        return Response({
            'items_total': count_items,
            'data': serializer.data,
        })

    @add_database_object_project
    def post(self, request, slug_project, database_object_project, use_sandbox, format=None):
        serializer = Serializer_Template_Worker(data=request.data)
        if serializer.is_valid():
            serializer.save(database_object_project=database_object_project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Template_Worker(APIView):
    permission_classes = PERMISSIONS_INSTANCE_ONLY

    @add_database_object_project
    def put(self, request, slug_project, database_object_project, use_sandbox, id_template, format=None):
        template = Manager_Templates_Worker.get(id_template)
        serializer = Serializer_Template_Worker(
            template,
            data=request.data,
            partial=True,
            context={
                'request': request,
                'usecase': 'list_templates_worker',
            }
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @add_database_object_project
    def delete(self, request, slug_project, database_object_project, use_sandbox, id_template, format=None):
        Manager_Templates_Worker.delete(id_template)
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes(PERMISSIONS_INSTANCE_ONLY)
@add_database_object_project
def templates_worker_all(request, slug_project, database_object_project, use_sandbox, format=None):
    list_fields = request.query_params.getlist('fields[]')
    if len(list_fields) == 0:
        list_fields = None

    queryset = Manager_Templates_Worker.get_all(
        database_object_project=database_object_project,
        request=request,
        fields=list_fields,
    )

    serializer = Serializer_Template_Worker(
        queryset,
        many=True,
        context={
            'usecase': 'templates_worker_all',
            'fields': list_fields,
        }
    )

    return Response(serializer.data)
