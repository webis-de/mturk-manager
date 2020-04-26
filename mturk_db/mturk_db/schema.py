import graphene

from api.modules.templates.queries import QueryTemplateAssignment


class Query(QueryTemplateAssignment, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
