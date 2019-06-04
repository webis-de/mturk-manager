from rest_framework import serializers


class Serializer_Config(serializers.Serializer):
    version = serializers.CharField()
    paths = serializers.DictField()

    class Meta:
        fields = (
            'version',
            'paths',
        )
