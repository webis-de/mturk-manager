from mturk_manager.models import m_Worker
from mturk_manager.serializers import Serializer_Worker
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# from rest_framework import viewsets
# class ViewSet_Workers(viewsets.ModelViewSet):
# # class ViewSet_Worker(viewsets.ReadOnlyModelViewSet):
#     queryset = m_Worker.objects.all()
#     serializer_class = Serializer_Worker



class Workers(APIView):
    def get(self, request, slug_project=None, format=None):
        workers = m_Worker.objects.all()
        # if slug_project != None:
        #     workers = workers.filter(fk_project)

        serializer = Serializer_Worker(workers, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = Serializer_Worker(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Worker(APIView):
    def get_object(self, name):
        try:
            return m_Worker.objects.get(name=name)
        except m_Worker.DoesNotExist:
            raise Http404

    def get(self, request, name, format=None):
        worker = self.get_object(name)
        serializer = Serializer_Worker(worker)
        return Response(serializer.data)

    def put(self, request, name, format=None):
        worker = self.get_object(name)
        serializer = Serializer_Worker(worker, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, name, format=None):
        worker = self.get_object(name)
        worker.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)