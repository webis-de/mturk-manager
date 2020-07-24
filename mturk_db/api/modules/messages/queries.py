import graphene
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from api.models import MessageReject
from api.modules.messages.types import TypeMessageReject


class QueryMessage(object):
    messages_reject = graphene.List(TypeMessageReject, project=graphene.ID())

    search_messages_reject = graphene.List(
        TypeMessageReject,
        message=graphene.String(required=True),
        limit=graphene.Int()
    )

    def resolve_messages_reject(self, info, project, **kwargs):
        queryset = MessageReject.objects.filter(projects=project)
        return queryset

    def resolve_search_messages_reject(self, info, message, limit=None, **kwargs):
        vector = SearchVector('message')
        query = SearchQuery(message)

        queryset = MessageReject.objects.annotate(
            rank=SearchRank(vector, query)
        ).order_by('-rank')

        if limit is not None:
            queryset = queryset[:limit]

        return queryset
