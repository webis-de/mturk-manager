from django.db.models import Count
from api.models import Project
from api.classes.messages import ManagerMessages
from api.models import MessageReject


class Manager_Messages_Reject(ManagerMessages):
    model = MessageReject
