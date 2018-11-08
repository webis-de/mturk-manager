from rest_framework import serializers
from api.models import Message_Reject

class Serializer_Message_Reject(serializers.ModelSerializer):
    count_usage = serializers.IntegerField(required=False)

    class Meta:
        model = Message_Reject
        fields = (
            'id', 
            'message', 
            'count_usage', 
        )
        extra_kwargs = {
            'id': {
                'read_only': False,
                'required': False,
            },
            # 'message': {
            #     'validators': [],
            # },
        }