from rest_framework import serializers
from api.models import Message_Reject


class Serializer_Config(serializers.Serializer):
    version_api = serializers.IntegerField()

    class Meta:
        fields = (
            'version_api',
        )
