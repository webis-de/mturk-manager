import graphene

from api.models import Template_Assignment
from api.modules.templates.types import TypeTemplateAssignment, TypeTemplateHIT, TypeTemplateGlobal


class QueryTemplateAssignment(object):
    templates_assignment = graphene.List(TypeTemplateAssignment)
    templates_hit = graphene.List(TypeTemplateHIT)
    templates_global = graphene.List(TypeTemplateGlobal)

    def resolve_templates_assignment(self, info, **kwargs):
        return Template_Assignment.objects.all()
