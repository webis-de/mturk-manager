from graphene_django import DjangoObjectType

from api.models import MessageReject, Reason, MessageApprove


class TypeMessageReject(DjangoObjectType):
    class Meta:
        model = MessageReject
        fields = '__all__'


class TypeMessageApprove(DjangoObjectType):
    class Meta:
        model = MessageApprove
        fields \
            = '__all__'


class TypeMessageReason(DjangoObjectType):
    class Meta:
        model = Reason
        fields = '__all__'
