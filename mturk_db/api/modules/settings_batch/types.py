from graphene_django import DjangoObjectType

from api.models import Settings_Batch


class TypeSettingsBatch(DjangoObjectType):
    class Meta:
        model = Settings_Batch
        fields = '__all__'
