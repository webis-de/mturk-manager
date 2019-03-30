from rest_framework import serializers
from api.models import Message_Reject


class Serializer_Config(serializers.Serializer):
    version = serializers.CharField()
    paths = serializers.DictField()

    class Meta:
        fields = (
            'version',
            'paths',
        )
