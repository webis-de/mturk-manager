import json
import graphene

from api.models import Template_Worker, Template_Assignment, Template_Global, Template_HIT, Project, Settings_Batch
from api.modules.settings_batch.types import TypeSettingsBatch
from api.modules.templates.helpers import count_parameters_in_template
from api.modules.templates.types import TypeTemplateAssignment, TypeTemplateWorker, TypeTemplateGlobal, TypeTemplateHIT


class InputSettingsBatch(graphene.InputObjectType):
    id = graphene.ID()
    project = graphene.Int(required=True)
    name = graphene.String(required=True)
    title = graphene.String()
    description = graphene.String()
    template_worker = graphene.ID()
    datetime_creation = graphene.DateTime()
    reward = graphene.Int()
    duration = graphene.Int()
    lifetime = graphene.Int()
    count_assignments = graphene.Int()
    count_assignments_max_per_worker = graphene.Int()
    block_workers = graphene.Boolean()
    has_content_adult = graphene.Boolean()
    qualification_assignments_approved = graphene.Int()
    qualification_hits_approved = graphene.Int()
    qualification_locale = graphene.String()
    # TODO
    # keywords = graphene.List()


'''
Create
'''


class MutationCreateSettingsBatch(graphene.Mutation):
    class Arguments:
        settings_batch = InputSettingsBatch(required=True)

    settings_batch = graphene.Field(TypeSettingsBatch)

    def mutate(self, info, settings_batch):
        settings_batch['project'] = Project.objects.get(id=settings_batch['project'])
        settings_batch['template_worker'] = Template_Worker.objects.get(id=settings_batch['template_worker'])

        settings_batch_new = Settings_Batch.objects.create(
            **settings_batch
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
