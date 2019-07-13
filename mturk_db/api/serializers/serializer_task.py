from rest_framework import serializers

from api.models import CeleryTasks


class SerializerTasks(serializers.ModelSerializer):

    payload = serializers.CharField(required=False)

    class Meta:
        model = CeleryTasks
        fields = (
            'id', 
            'project',
            'task',
            'description',
            'status',

            'datetime_created',
            'datetime_started',
            'datetime_finished',

            'payload',
        )
        extra_kwargs = {
        }