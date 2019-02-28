from api.classes import Interface_Manager_Items
from api.models import Keyword


class Manager_Keywords(Interface_Manager_Items):
    @staticmethod
    def get_all(database_object_project, request, fields=None):
        return Keyword.objects.all()
