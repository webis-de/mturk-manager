import graphene
from graphene_django import DjangoObjectType

from api.models import Template_Assignment, Template_HIT, Template_Global, Template_Worker, Project, Template

# TODO move to project
class TypeProject(DjangoObjectType):
    class Meta:
        model = Project
        fields = '__all__'


class TypeTemplateWorker(DjangoObjectType):
    class Meta:
        model = Template_Worker
        fields = '__all__'


class TypeTemplateAssignment(DjangoObjectType):
    class Meta:
        model = Template_Assignment
        fields = '__all__'


class TypeTemplateHIT(DjangoObjectType):
    class Meta:
        model = Template_HIT
        fields = '__all__'


class TypeTemplateGlobal(DjangoObjectType):
    class Meta:
        model = Template_Global
        fields = '__all__'
