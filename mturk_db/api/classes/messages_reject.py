from django.db.models import Count

from api.classes import Interface_Manager_Items
from api.models import Message_Reject


class Manager_Messages_Reject(Interface_Manager_Items):
    @staticmethod
    def get_all(database_object_project, request, fields=None):
        return Message_Reject.objects.all().annotate(
            count_usage=Count('project', distinct=True)
        )
