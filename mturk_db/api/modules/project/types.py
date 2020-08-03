from graphene_django import DjangoObjectType

from api.models import Project


class TypeProject(DjangoObjectType):
    class Meta:
        model = Project
        fields = '__all__'
