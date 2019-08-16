from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from api.classes import Manager_Templates_HIT
from api.helpers import add_database_object_project, paginate_queryset
from api.models import Template_HIT as Model_Template_HIT
from api.serializers import Serializer_Template_HIT
from mturk_db.permissions import IsInstance, IsWorker, AllowOptionsAuthentication
from mturk_db.settings import REST_FRAMEWORK

PERMISSIONS_INSTANCE_ONLY = (AllowOptionsAuthentication, IsInstance,)
PERMISSIONS_WORKER_ONLY = (AllowOptionsAuthentication, IsWorker,)


class Templates_HIT(APIView):
    permission_classes = PERMISSIONS_INSTANCE_ONLY

    @add_database_object_project
    def get(self, request, slug_project, database_object_project, use_sandbox, format=None):
        queryset, list_fields = Manager_Templates_HIT.get_all(
            database_object_project=database_object_project,
            request=request,
        )

        queryset_paginated, count_items = paginate_queryset(queryset, request)

        serializer = Serializer_Template_HIT(
            queryset_paginated,
            many=True,
            context={
                'request': request,
                'usecase': 'list_templates_hit',
                'fields': list_fields,
            }
        )

        return Response({
            'items_total': count_items,
            'data': serializer.data,
        })

    @add_database_object_project
    def post(self, request, slug_project, database_object_project, use_sandbox, format=None):
        serializer = Serializer_Template_HIT(data=request.data)
        if serializer.is_valid():
            serializer.save(database_object_project=database_object_project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Template_HIT(APIView):
    permission_classes = PERMISSIONS_INSTANCE_ONLY

    @add_database_object_project
    def put(self, request, slug_project, database_object_project, use_sandbox, id_template, format=None):
        template = Manager_Templates_HIT.get(id_template)
        serializer = Serializer_Template_HIT(template, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def get_object(self, slug):
#         try:
#             return m_Project.objects.get(slug=slug)
#         except m_Project.DoesNotExist:
#             raise Http404

#     # def get(self, request, name, format=None):
#     #     project = self.get_object(name)
#     #     serializer = Serializer_Template_Worker(project, context={'request': request})
#     #     return Response(serializer.data)

#     @add_database_object_project
#     def put(self, request, slug_project, database_object_project, use_sandbox, format=None):
#         print('####')
#         print(request.data)
#         project = self.get_object(slug_project)
#         serializer = Serializer_Template_Worker(project, data=request.data, partial=True)
#         print(serializer)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @add_database_object_project
    def delete(self, request, slug_project, database_object_project, use_sandbox, id_template, format=None):
        Manager_Templates_HIT.delete(id_template)
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes(PERMISSIONS_INSTANCE_ONLY)
@add_database_object_project
def templates_hit_all(request, slug_project, database_object_project, use_sandbox, format=None):
    queryset, list_fields = Manager_Templates_HIT.get_all(
        database_object_project=database_object_project,
        request=request,
    )

    serializer = Serializer_Template_HIT(
        queryset,
        many=True,
        context={
            'usecase': 'templates_hit_all',
            'fields': list_fields,
        }
    )

    return Response(serializer.data)
