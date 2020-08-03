import graphene

from api.models import Settings_Batch
from api.modules.settings_batch.types import TypeSettingsBatch


class QuerySettingsBatch(object):
    settings_batch = graphene.List(TypeSettingsBatch, project=graphene.ID())

    def resolve_settings_batch(self, info, project, **kwargs):
        return Settings_Batch.objects.filter(
            project=project,
            batch=None
        )
