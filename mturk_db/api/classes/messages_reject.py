from django.db.models import Count
from api.models import Project
from api.classes.messages import ManagerMessages
from api.models import MessageReject


class Manager_Messages_Reject(ManagerMessages):
    model = MessageReject

    @classmethod
    def create(cls, data: dict, database_object_project: Project = None) -> MessageReject:
        print(data)
        print(database_object_project)

        message = data.get('message')
        if message is not None:
            instance, was_created = cls.model.objects.get_or_create(
                message=message,
                message_lowercase=message.lower(),
            )
        else:
            instance = cls.model.objects.get(id=data.get('id'))

        instance.projects.add(database_object_project)

        return instance
