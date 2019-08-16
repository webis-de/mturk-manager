import json

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from api.classes import Manager_HITs
from api.helpers import add_database_object_project, paginate_queryset
from api.serializers import Serializer_HIT
from mturk_db.permissions import IsInstance, AllowOptionsAuthentication
from mturk_db.settings import REST_FRAMEWORK

PERMISSIONS_INSTANCE_ONLY = (AllowOptionsAuthentication, IsInstance,)


class HITs(APIView):
    permission_classes = PERMISSIONS_INSTANCE_ONLY

    def get(self, request):
        try:
            use_sandbox = False if request.query_params['use_sandbox'] == 'false' else True
        except KeyError:
            use_sandbox = True

        queryset, list_fields = Manager_HITs.get_all(
            request=request,
            use_sandbox=use_sandbox
        )

        queryset_paginated, count_items = paginate_queryset(queryset, request)

        serializer = Serializer_HIT(
            queryset_paginated,
            many=True,
            context={
                'request': request,
                'fields': list_fields,
            }
        )

        return Response({
            'items_total': count_items,
            'data': serializer.data,
        })


class ProjectHITs(APIView):
    permission_classes = PERMISSIONS_INSTANCE_ONLY

    @add_database_object_project
    def get(self, request, slug_project, database_object_project, use_sandbox, format=None):
        queryset, list_fields = Manager_HITs.get_all(
            database_object_project=database_object_project,
            use_sandbox=use_sandbox,
            request=request
        )

        queryset_paginated, count_items = paginate_queryset(queryset, request)

        serializer = Serializer_HIT(
            queryset_paginated,
            many=True,
            context={
                'usecase': 'list_hits',
                'fields': list_fields,
            }
        )

        return Response({
            'items_total': count_items,
            'data': serializer.data,
        })


@api_view(['GET'])
@permission_classes(PERMISSIONS_INSTANCE_ONLY)
@add_database_object_project
def hits_for_annotation(request, slug_project, database_object_project, use_sandbox, format=None):
    queryset, list_fields = Manager_HITs.get_all(
        database_object_project=database_object_project,
        use_sandbox=use_sandbox,
        request=request
    )

    serializer = Serializer_HIT(
        queryset,
        context={
            'usecase': 'annotation',
            'fields': list_fields,
        },
        many=True
    )

    return Response(serializer.data)
