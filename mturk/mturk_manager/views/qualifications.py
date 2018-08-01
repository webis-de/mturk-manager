from mturk_manager.models import Model_Qualification
from mturk_manager.serializers import Serializer_Qualification
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mturk_manager.classes import Manager_Qualifications
from mturk_manager.helpers import add_database_object_project
from urllib.parse import parse_qs

class Qualifications(APIView):
    @add_database_object_project
    def get(self, request, slug_project, database_object_project, use_sandbox, format=None):
        print(use_sandbox)
        print(use_sandbox)
        print(use_sandbox)
        print(use_sandbox)
        print(use_sandbox)
        list_qualifications = Manager_Qualifications.get_all(database_object_project, use_sandbox)
        serializer = Serializer_Qualification(list_qualifications, many=True, context={'request': request})
        return Response(serializer.data)

    @add_database_object_project
    def post(self, request, slug_project, database_object_project, use_sandbox, format=None):
        print(request.data)
        serializer = Serializer_Qualification(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save(database_object_project=database_object_project, use_sandbox=use_sandbox)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @add_database_object_project
    def delete(self, request, slug_project, database_object_project, use_sandbox, format=None):
        try:
            list_ids = parse_qs(request.META['QUERY_STRING'])['ids']
        except KeyError:
            return Response(status=status.HTTP_204_NO_CONTENT)

        count_deleted = Manager_Qualifications.delete(database_object_project=database_object_project, use_sandbox=use_sandbox, list_ids=list_ids)
        return Response(status=status.HTTP_204_NO_CONTENT)

@add_database_object_project
def import_qualifications(self, request, slug_project, database_object_project):
    print(request)

class Qualification(APIView):
    def get_object(self, name):
        try:
            return Model_Qualification.objects.get(name=name)
        except Model_Qualification.DoesNotExist:
            raise Http404

    # def get(self, request, name, format=None):
    #     qualification = self.get_object(name)
    #     serializer = Serializer_Qualification(qualification, context={'request': request})
    #     return Response(serializer.data)

    @add_database_object_project
    def put(self, request, slug_project, database_object_project, use_sandbox, id_mturk, format=None):
        serializer = Serializer_Qualification(request.data, data=request.data)
        if serializer.is_valid():
            serializer.save(database_object_project=database_object_project, use_sandbox=use_sandbox, id_mturk=id_mturk)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @add_database_object_project
    # def delete(self, request, slug_project, database_object_project, use_sandbox, format=None):
    #     print('delete')
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    #     qualification = self.get_object(name)
    #     qualification.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)