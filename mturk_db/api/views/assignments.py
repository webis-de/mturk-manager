import json

from rest_framework.settings import api_settings

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

class Assignments(APIView):
    permission_classes = PERMISSIONS_INSTANCE_ONLY

    @add_database_object_project
    def get(self, request, slug_project, database_object_project, use_sandbox, format=None):
        queryset = Manager_Assignments.get_all(
            database_object_project=database_object_project,
            use_sandbox=use_sandbox,
            request=request
        )

        queryset_paginated = queryset

        if request.query_params.get(REST_FRAMEWORK['PAGE_SIZE_QUERY_PARAM']) is not None:
            paginator = api_settings.DEFAULT_PAGINATION_CLASS()
            queryset_paginated = paginator.paginate_queryset(queryset, request)

        serializer = Serializer_Assignment(
            queryset_paginated,
            many=True,
            context={
                'usecase': 'list_assignments'
            })

        return Response({
            'items_total': queryset.count(),
            'data': serializer.data,
        })
    # @add_database_object_project
    # def get(self, request, slug_project, database_object_project, use_sandbox, format=None):
    #     list_ids = json.loads(request.query_params.get('list_ids', '[]'))
    #
    #     queryset_assignments = Manager_Assignments.get_all(database_object_project=database_object_project, use_sandbox=use_sandbox, list_ids=list_ids)
    #     # queryset_projects = m_Project.objects.all()
    #     # serializer = Serializer_Project(queryset_projects, many=True, context={'request': request})
    #     serializer = Serializer_Assignment(queryset_assignments, many=True)
    #     return Response(serializer.data)

    @add_database_object_project
    def put(self, request, slug_project, database_object_project, use_sandbox, format=None):
        Manager_Assignments.update_stati_assignments(database_object_project, request.data)
        # assignment = self.get_object(id_assignment)
        # print(request)
        # print(request.data)

        # print(request)
        return Response({})
        # serializer = Serializer_Assignment(assignment, data=request.data, many=True, partial=True)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @add_database_object_project
    # def post(self, request, slug_project, database_object_project, use_sandbox, format=None):
    #     serializer = Serializer_Batch(data=request.data)
    #     print(serializer)
    #     if serializer.is_valid():
    #         serializer.save(database_object_project=database_object_project, use_sandbox=use_sandbox)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @add_database_object_project
    # def patch(self, request, slug_project, database_object_project, use_sandbox, format=None):
    #     list_batches_changed = Manager_Batches.sync_mturk(database_object_project, use_sandbox)
    #     serializer = Serializer_Batch(list_batches_changed, many=True)

    #     # serializer = Serializer_Batch(data=request.data)
    #     return Response(serializer.data)

@api_view(['GET'])
@permission_classes(PERMISSIONS_INSTANCE_ONLY)
@add_database_object_project
def assignments_for_annotation(request, slug_project, database_object_project, use_sandbox, format=None):
    queryset_assignments = Manager_Assignments.get_all(
        database_object_project=database_object_project,
        use_sandbox=use_sandbox,
        request=request
    )

    serializer = Serializer_Assignment(
        queryset_assignments,
        context={
            'usecase': 'annotation'
        },
        many=True
    )

    return Response(serializer.data)

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