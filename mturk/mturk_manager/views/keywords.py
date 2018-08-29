from mturk_manager.models import Keyword
from mturk_manager.serializers import Serializer_Keyword
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from mturk_manager.helpers import add_database_object_project

class Keywords(APIView):
    # @add_database_object_project
    def get(self, request, format=None):
        queryset_keywords = Keyword.objects.all()
        serializer = Serializer_Keyword(queryset_keywords, many=True, context={'request': request})
        return Response(serializer.data)

    # def post(self, request, format=None):
    #     serializer = Serializer_Project(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class Project(APIView):
#     def get_object(self, slug):
#         try:
#             return m_Project.objects.get(slug=slug)
#         except m_Project.DoesNotExist:
#             raise Http404

#     # def get(self, request, name, format=None):
#     #     project = self.get_object(name)
#     #     serializer = Serializer_Project(project, context={'request': request})
#     #     return Response(serializer.data)

#     @add_database_object_project
#     def put(self, request, slug_project, database_object_project, use_sandbox, format=None):
#         print('####')
#         print(request.data)
#         project = self.get_object(slug_project)
#         serializer = Serializer_Project(project, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     # def delete(self, request, name, format=None):
#     #     project = self.get_object(name)
#     #     project.delete()
#     #     return Response(status=status.HTTP_204_NO_CONTENT)