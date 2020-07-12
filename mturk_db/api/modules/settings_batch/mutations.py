import json
import graphene

from api.models import Template_Worker, Template_Assignment, Template_Global, Template_HIT, Project, Settings_Batch
from api.modules.settings_batch.types import TypeSettingsBatch
from api.modules.templates.helpers import count_parameters_in_template
from api.modules.templates.types import TypeTemplateAssignment, TypeTemplateWorker, TypeTemplateGlobal, TypeTemplateHIT


class InputSettingsBatch(object):
    id = graphene.Int()
    name = graphene.String(required=True)
    project = graphene.Int(required=True)
    template = graphene.String(required=True)
    is_active = graphene.Boolean(required=True)
    datetime_creation = graphene.DateTime()


'''
Create
'''


class MutationCreateSettingsBatch(graphene.Mutation):
    class Arguments:
        settings_batch = InputSettingsBatch(required=True)

    settings_batch = graphene.Field(TypeSettingsBatch)

    def mutate(self, info, settings_batch):
        project = Project.objects.get(id=template['project'])
        templateAssignment = Template_Assignment.objects.get(id=template['template_assignment']) if template['template_assignment'] is not None else None
        templateHIT = Template_HIT.objects.get(id=template['template_hit']) if template['template_hit'] is not None else None
        templateGlobal = Template_Global.objects.get(id=template['template_global']) if template['template_global'] is not None else None

        settings_batch_new = Template_Worker.objects.create(
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

        return MutationCreateSettingsBatch(settings_batch=settings_batch_new)


'''
Update
'''


class MutationUpdateSettingsBatch(graphene.Mutation):
    class Arguments:
        settings_batch = InputSettingsBatch(required=True)

    template = graphene.Field(TypeTemplateWorker)

    def mutate(self, info, settings_batch):
        template = Template_Worker.objects.get(id=settings_batch['template']) if settings_batch['template'] is not None else None

        settings_batch_updated = Settings_Batch.objects.filter(
            id=settings_batch.id,
        )

        settings_batch_updated.update(
            name=settings_batch['name'],
            template=template,
        )

        return MutationUpdateSettingsBatch(template=settings_batch_updated.first())

'''
Delete
'''


class MutationDeleteSettingsBatch(graphene.Mutation):
    class Arguments:
        id_settings_batch = graphene.ID(required=True)

    id_settings_batch = graphene.ID()

    def mutate(self, info, id_settings_batch):
        Settings_Batch.objects.filter(
            id=id_settings_batch,
        ).delete()

        return MutationDeleteSettingsBatch(id_settings_batch=id_settings_batch)


class MutationSettingsBatch(graphene.ObjectType):
    create_settings_batch = MutationCreateSettingsBatch.Field()

    update_settings_batch = MutationUpdateSettingsBatch.Field()

    delete_settings_batch = MutationDeleteSettingsBatch.Field()
