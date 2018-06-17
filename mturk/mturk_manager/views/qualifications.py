from mturk_manager.models import Model_Qualification
from mturk_manager.serializers import Serializer_Qualification
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mturk_manager.classes import Manager_Qualifications
from mturk_manager.helpers import add_database_object_project

class Qualifications(APIView):
    @add_database_object_project
    def get(self, request, slug_project, database_object_project, format=None):
        dictionary_qualifications = Manager_Qualifications.get_all(database_object_project)
        serializer = Serializer_Qualification(dictionary_qualifications, many=True, context={'request': request})
        return Response(serializer.data)

    @add_database_object_project
    def post(self, request, database_object_project, format=None):
        serializer = Serializer_Qualification(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Qualification(APIView):
    def get_object(self, name):
        try:
            return Model_Qualification.objects.get(name=name)
        except Model_Qualification.DoesNotExist:
            raise Http404

    def get(self, request, name, format=None):
        qualification = self.get_object(name)
        serializer = Serializer_Qualification(qualification, context={'request': request})
        return Response(serializer.data)

    def put(self, request, name, format=None):
        qualification = self.get_object(name)
        serializer = Serializer_Qualification(qualification, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, name, format=None):
        qualification = self.get_object(name)
        qualification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)