import json
import graphene

from api.models import Template_Worker, Template_Assignment, Template_Global, Template_HIT, Project
from api.modules.templates.helpers import count_parameters_in_template
from api.modules.templates.types import TypeTemplateAssignment, TypeTemplateWorker, TypeTemplateGlobal, TypeTemplateHIT


class InputTemplateBase(object):
    id = graphene.Int()
    name = graphene.String(required=True)
    project = graphene.Int(required=True)
    template = graphene.String(required=True)
    is_active = graphene.Boolean(required=True)
    datetime_creation = graphene.DateTime()


class InputTemplateWorker(InputTemplateBase, graphene.InputObjectType):
    height_frame = graphene.Int(required=True)
    template_assignment = graphene.Int()
    template_hit = graphene.Int()
    template_global = graphene.Int()
    json_dict_parameters = graphene.String(required=True)
    template_original = graphene.Int()


class InputTemplateAssignment(InputTemplateBase, graphene.InputObjectType):
    pass


class InputTemplateHIT(InputTemplateBase, graphene.InputObjectType):
    pass


class InputTemplateGlobal(InputTemplateBase, graphene.InputObjectType):
    pass


'''
Create
'''


class MutationCreateTemplateWorker(graphene.Mutation):
    class Arguments:
        template = InputTemplateWorker(required=True)

    template = graphene.Field(TypeTemplateWorker)

    def mutate(self, info, template):
        project = Project.objects.get(id=template['project'])
        templateAssignment = Template_Assignment.objects.get(id=template['template_assignment']) if template['template_assignment'] is not None else None
        templateHIT = Template_HIT.objects.get(id=template['template_hit']) if template['template_hit'] is not None else None
        templateGlobal = Template_Global.objects.get(id=template['template_global']) if template['template_global'] is not None else None

        template = Template_Worker.objects.create(
            name=template['name'],
            project=project,
            template=template['template'],
            is_active=template.get('is_active'),
            height_frame=template['height_frame'],
            template_assignment=templateAssignment,
            template_hit=templateHIT,
            template_global=templateGlobal,
            json_dict_parameters=json.dumps(count_parameters_in_template(template['template'])),
        )

        return MutationCreateTemplateWorker(template=template)


class MutationCreateTemplateAssignment(graphene.Mutation):
    class Arguments:
        template = InputTemplateAssignment(required=True)

    template = graphene.Field(TypeTemplateAssignment)

    def mutate(self, info, template):
        project = Project.objects.get(id=template['project'])

        template = Template_Assignment.objects.create(
            name=template['name'],
            project=project,
            template=template['template'],
        )

        return MutationCreateTemplateAssignment(template=template)


class MutationCreateTemplateHIT(graphene.Mutation):
    class Arguments:
        template = InputTemplateHIT(required=True)

    template = graphene.Field(TypeTemplateHIT)

    def mutate(self, info, template):
        project = Project.objects.get(id=template['project'])

        template = Template_HIT.objects.create(
            name=template['name'],
            project=project,
            template=template['template'],
        )

        return MutationCreateTemplateHIT(template=template)


class MutationCreateTemplateGlobal(graphene.Mutation):
    class Arguments:
        template = InputTemplateGlobal(required=True)

    template = graphene.Field(TypeTemplateGlobal)

    def mutate(self, info, template):
        project = Project.objects.get(id=template['project'])

        template = Template_Global.objects.create(
            name=template['name'],
            project=project,
            template=template['template'],
        )

        return MutationCreateTemplateGlobal(template=template)


'''
Update
'''


class MutationUpdateTemplateWorker(graphene.Mutation):
    class Arguments:
        template = InputTemplateWorker(required=True)

    template = graphene.Field(TypeTemplateWorker)

    def mutate(self, info, template):
        templateAssignment = Template_Assignment.objects.get(id=template['template_assignment']) if template['template_assignment'] is not None else None
        templateHIT = Template_HIT.objects.get(id=template['template_hit']) if template['template_hit'] is not None else None
        templateGlobal = Template_Global.objects.get(id=template['template_global']) if template['template_global'] is not None else None

        templateUpdated = Template_Worker.objects.filter(
            id=template.id,
        )
        print(template)
        templateUpdated.update(
            name=template['name'],
            template=template['template'],
            is_active=template.get('is_active'),
            height_frame=template['height_frame'],
            template_assignment=templateAssignment,
            template_hit=templateHIT,
            template_global=templateGlobal,
            json_dict_parameters=json.dumps(count_parameters_in_template(template['template'])),
        )

        return MutationUpdateTemplateWorker(template=templateUpdated.first())


class MutationUpdateTemplateAssignment(graphene.Mutation):
    class Arguments:
        template = InputTemplateAssignment(required=True)

    template = graphene.Field(TypeTemplateAssignment)

    def mutate(self, info, template):
        templateUpdated = Template_Assignment.objects.filter(
            id=template.id,
        )

        templateUpdated.update(
            name=template['name'],
            template=template['template'],
        )

        return MutationUpdateTemplateAssignment(template=templateUpdated.first())


class MutationUpdateTemplateHIT(graphene.Mutation):
    class Arguments:
        template = InputTemplateHIT(required=True)

    template = graphene.Field(TypeTemplateHIT)

    def mutate(self, info, template):
        templateUpdated = Template_HIT.objects.filter(
            id=template.id,
        )

        templateUpdated.update(
            name=template['name'],
            template=template['template'],
        )

        return MutationUpdateTemplateHIT(template=templateUpdated.first())


class MutationUpdateTemplateGlobal(graphene.Mutation):
    class Arguments:
        template = InputTemplateGlobal(required=True)

    template = graphene.Field(TypeTemplateGlobal)

    def mutate(self, info, template):
        templateUpdated = Template_Global.objects.filter(
            id=template.id,
        )

        templateUpdated.update(
            name=template['name'],
            template=template['template'],
        )

        return MutationUpdateTemplateGlobal(template=templateUpdated.first())


'''
Delete
'''


class MutationDeleteTemplateWorker(graphene.Mutation):
    class Arguments:
        id_template = graphene.ID(required=True)

    id_template = graphene.ID()

    def mutate(self, info, id_template):
        Template_Worker.objects.filter(
            id=id_template,
        ).delete()

        return MutationDeleteTemplateWorker(id_template=id_template)


class MutationDeleteTemplateAssignment(graphene.Mutation):
    class Arguments:
        id_template = graphene.ID(required=True)

    id_template = graphene.ID()

    def mutate(self, info, id_template):
        Template_Assignment.objects.filter(
            id=id_template,
        ).delete()

        return MutationDeleteTemplateAssignment(id_template=id_template)


class MutationDeleteTemplateHIT(graphene.Mutation):
    class Arguments:
        id_template = graphene.ID(required=True)

    id_template = graphene.ID()

    def mutate(self, info, id_template):
        Template_HIT.objects.filter(
            id=id_template,
        ).delete()

        return MutationDeleteTemplateHIT(id_template=id_template)


class MutationDeleteTemplateGlobal(graphene.Mutation):
    class Arguments:
        id_template = graphene.ID(required=True)

    id_template = graphene.ID()

    def mutate(self, info, id_template):
        Template_Global.objects.filter(
            id=id_template,
        ).delete()

        return MutationDeleteTemplateGlobal(id_template=id_template)


class MutationTemplate(graphene.ObjectType):
    create_template_worker = MutationCreateTemplateWorker.Field()
    create_template_assignment = MutationCreateTemplateAssignment.Field()
    create_template_hit = MutationCreateTemplateHIT.Field()
    create_template_global = MutationCreateTemplateGlobal.Field()

    update_template_worker = MutationUpdateTemplateWorker.Field()
    update_template_assignment = MutationUpdateTemplateAssignment.Field()
    update_template_hit = MutationUpdateTemplateHIT.Field()
    update_template_global = MutationUpdateTemplateGlobal.Field()

    delete_template_worker = MutationDeleteTemplateWorker.Field()
    delete_template_assignment = MutationDeleteTemplateAssignment.Field()
    delete_template_hit = MutationDeleteTemplateHIT.Field()
    delete_template_global = MutationDeleteTemplateGlobal.Field()
