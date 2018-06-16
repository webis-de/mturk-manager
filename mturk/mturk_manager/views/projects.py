from mturk_manager.models import m_Project
from mturk_manager.serializers import Serializer_Project
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# from rest_framework import viewsets
# class ViewSet_Projects(viewsets.ModelViewSet):
# # class ViewSet_Worker(viewsets.ReadOnlyModelViewSet):
#     queryset = m_Project.objects.all()
#     serializer_class = Serializer_Project

class Projects(APIView):
    def get(self, request, format=None):
        project = m_Project.objects.all()
        serializer = Serializer_Project(project, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = Serializer_Project(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Project(APIView):
    def get_object(self, name):
        try:
            return m_Project.objects.get(name=name)
        except m_Project.DoesNotExist:
            raise Http404

    def get(self, request, name, format=None):
        project = self.get_object(name)
        serializer = Serializer_Project(project, context={'request': request})
        return Response(serializer.data)

    def put(self, request, name, format=None):
        project = self.get_object(name)
        serializer = Serializer_Project(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, name, format=None):
        project = self.get_object(name)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)