from mturk_manager.models import m_Worker
from mturk_manager.serializers import Serializer_Worker
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mturk_manager.helpers import add_database_object_project
from rest_framework.decorators import api_view
from mturk_manager.classes import Manager_Workers

# from rest_framework import viewsets
# class ViewSet_Workers(viewsets.ModelViewSet):
# # class ViewSet_Worker(viewsets.ReadOnlyModelViewSet):
#     queryset = m_Worker.objects.all()
#     serializer_class = Serializer_Worker



class Workers(APIView):
    @add_database_object_project
    def get(self, request, slug_project, database_object_project, use_sandbox, format=None):
        querset_workers = Manager_Workers.get_all(database_object_project, use_sandbox)
        # if slug_project != None:
        #     workers = workers.filter(fk_project__slug=slug_project)

        serializer = Serializer_Worker(querset_workers, many=True)
        return Response(serializer.data)

    # def post(self, request, format=None):
    #     serializer = Serializer_Worker(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@add_database_object_project
def get_status_block(request, slug_project, database_object_project, use_sandbox, format=None):
    dictionary_data = Manager_Workers.get_status_block(database_object_project, use_sandbox)
    return Response(dictionary_data)

# @api_view(['PUT'])
# @add_database_object_project
# def update(request, slug_project, database_object_project, use_sandbox, name, format=None):
#     Manager_Workers.update(database_object_project, use_sandbox, name, request.data)

class Worker(APIView):
    def get_object(self, name):
        try:
            return m_Worker.objects.get(name=name)
        except m_Worker.DoesNotExist:
            raise Http404


    # def get(self, request, name, format=None):
    #     worker = self.get_object(name)
    #     serializer = Serializer_Worker(worker)
    #     return Response(serializer.data)

    @add_database_object_project
    def put(self, request, slug_project, database_object_project, use_sandbox, name, format=None):
        serializer = Serializer_Worker(request.data, data=request.data)
        if serializer.is_valid():
            serializer.save(database_object_project=database_object_project, use_sandbox=use_sandbox, name=name)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # print(request.data)
        # serializer = Serializer_Worker(request.data, data=request.data)
        # print(serializer)
        # return
        # worker = self.get_object(name)
        # serializer = Serializer_Worker(worker, data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, name, format=None):
    #     worker = self.get_object(name)
    #     worker.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)