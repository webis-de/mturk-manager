import graphene

from api.models import Template_Assignment, Template_HIT, Template_Global, Template_Worker
from api.modules.templates.types import TypeTemplateAssignment, TypeTemplateHIT, TypeTemplateGlobal, TypeTemplateWorker


class QueryTemplate(object):
    templates_worker = graphene.List(TypeTemplateWorker, project=graphene.ID())
    templates_assignment = graphene.List(TypeTemplateAssignment, project=graphene.ID())
    templates_hit = graphene.List(TypeTemplateHIT, project=graphene.ID())
    templates_global = graphene.List(TypeTemplateGlobal, project=graphene.ID())

    def resolve_templates_worker(self, info, project, **kwargs):
        return Template_Worker.objects.filter(
            project=project,
            template_original=None,
        )

    def resolve_templates_assignment(self, info, project, **kwargs):
        return Template_Assignment.objects.filter(
            project=project,
        )

    def resolve_templates_hit(self, info, project, **kwargs):
        return Template_HIT.objects.filter(
            project=project,
        )

    def resolve_templates_global(self, info, project, **kwargs):
        return Template_Global.objects.filter(
            project=project,
        )
