import graphene

from api.modules.templates.mutations import MutationTemplate
from api.modules.templates.queries import QueryTemplateAssignment


class Query(QueryTemplateAssignment, graphene.ObjectType):
    pass


class Mutation(MutationTemplate, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
