from rest_framework import serializers
from api.models import Message_Reject


class Serializer_Config(serializers.Serializer):
    version_api = serializers.FloatField()
    paths = serializers.DictField()

    class Meta:
        fields = (
            'version_api',
            'paths',
        )
