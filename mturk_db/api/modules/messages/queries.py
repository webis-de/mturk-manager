import graphene
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import Count

from api.models import MessageReject
from api.modules.messages.types import TypeMessageReject


class QueryMessage(object):
    messages_reject = graphene.List(TypeMessageReject, project=graphene.ID(), limit=graphene.Int())

    search_messages_reject = graphene.List(
        TypeMessageReject,
        message=graphene.String(required=True),
        limit=graphene.Int()
    )

    def resolve_messages_reject(self, info, project=None, limit=None, **kwargs):
        queryset = MessageReject.objects.all()

        if project is not None:
            queryset = queryset.filter(projects=project)
        else:
            queryset = queryset.annotate(
                count_usage=Count('project', distinct=True) + Count('projects', distinct=True),
            ).order_by('-count_usage')

        if limit is not None:
            queryset = queryset[:limit]

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
