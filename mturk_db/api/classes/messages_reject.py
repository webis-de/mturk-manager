from django.db.models import Count

from api.classes.messages import ManagerMessages
from api.models import MessageReject


class Manager_Messages_Reject(ManagerMessages):
    model = MessageReject

    # @staticmethod
    # def get_all(database_object_project, request, fields=None):
    #     return MessageReject.objects.all().annotate(
    #         count_usage=Count('project', distinct=True)
    #     )
