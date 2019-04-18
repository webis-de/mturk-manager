import json

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from api.classes import Manager_HITs
from api.helpers import add_database_object_project
from api.serializers import Serializer_HIT
from mturk_db.permissions import IsInstance, AllowOptionsAuthentication
from mturk_db.settings import REST_FRAMEWORK

PERMISSIONS_INSTANCE_ONLY = (AllowOptionsAuthentication, IsInstance,)


class HITs(APIView):
    permission_classes = PERMISSIONS_INSTANCE_ONLY

    @add_database_object_project
    def get(self, request, slug_project, database_object_project, use_sandbox, format=None):
        queryset = Manager_HITs.get_all(
            database_object_project=database_object_project,
            use_sandbox=use_sandbox,
            request=request
        )

        queryset_paginated = queryset

        if request.query_params.get(REST_FRAMEWORK['PAGE_SIZE_QUERY_PARAM']) is not None:
            paginator = api_settings.DEFAULT_PAGINATION_CLASS()
            queryset_paginated = paginator.paginate_queryset(queryset, request)
            count_items = paginator.page.paginator.count
        else:
            count_items = queryset.count()

        serializer = Serializer_HIT(
            queryset_paginated,
            many=True,
            context={
                'usecase': 'list_hits'
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
    queryset = Manager_HITs.get_all(
        database_object_project=database_object_project,
        use_sandbox=use_sandbox,
        request=request
    )

    serializer = Serializer_HIT(
        queryset,
        context={
            'usecase': 'annotation',
        },
        many=True
    )

    return Response(serializer.data)
