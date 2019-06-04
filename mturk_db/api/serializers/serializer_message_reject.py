from rest_framework import serializers

from api.classes import Manager_Messages_Reject
from api.models import MessageReject

class Serializer_Message_Reject(serializers.ModelSerializer):
    count_usage = serializers.IntegerField(required=False)

    class Meta:
        model = MessageReject
        fields = (
            'id', 
            'message', 
            'message_lowercase',
            'count_usage',
        )
        extra_kwargs = {
            'id': {
                'read_only': False,
                'required': False,
            },
            'message': {
                'required': False,
            },
            'message_lowercase': {
                'required': False,
                'validators': []
            },
        }

    def create(self, validated_data):
        print('validated_data')
        print(validated_data)

        item = Manager_Messages_Reject.create(
            database_object_project=validated_data.get('database_object_project'),
            data=validated_data
        )

        return item
