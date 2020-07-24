import graphene

from api.models import MessageReject, Project
from api.modules.messages.types import TypeMessageReject


class InputMessageBase(graphene.InputObjectType):
    id = graphene.ID()
    project = graphene.ID()
    projects = graphene.List(graphene.ID, required=True)
    message = graphene.String(required=True)


class InputMessageReject(InputMessageBase, graphene.InputObjectType):
    pass


'''
Create
'''


class MutationCreateMessageReject(graphene.Mutation):
    class Arguments:
        message = InputMessageReject(required=True)

    message = graphene.Field(TypeMessageReject)

    def mutate(self, info, message):
        message_new = MessageReject.objects.create(
            message=message['message'],
        )

        for id_project in message['projects']:
            project = Project.objects.get(id=id_project)
            message_new.projects.add(project)

        return MutationCreateMessageReject(message=message_new)


'''
Delete
'''


class MutationDeleteMessageReject(graphene.Mutation):
    class Arguments:
        id_message = graphene.ID(required=True)

    id_message = graphene.ID()

    def mutate(self, info, id_message):
        MessageReject.objects.filter(
            id=id_message,
        ).delete()

        return MutationDeleteMessageReject(id_message=id_message)


class MutationMessage(graphene.ObjectType):
    create_message_reject = MutationCreateMessageReject.Field()

    delete_message_reject = MutationDeleteMessageReject.Field()
