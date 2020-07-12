import graphene

from api.modules.keywords.queries import QueryKeyword
from api.modules.project.queries import QueryProject
from api.modules.settings_batch.queries import QuerySettingsBatch
from api.modules.templates.mutations import MutationTemplate
from api.modules.templates.queries import QueryTemplate


class Query(QueryProject, QueryTemplate, QuerySettingsBatch, QueryKeyword, graphene.ObjectType):
    pass


class Mutation(MutationTemplate, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
