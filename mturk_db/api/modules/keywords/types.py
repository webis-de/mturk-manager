from graphene_django import DjangoObjectType

from api.models import Keyword


class TypeKeyword(DjangoObjectType):
    class Meta:
        model = Keyword
        fields = '__all__'
