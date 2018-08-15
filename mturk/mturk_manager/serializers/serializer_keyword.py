from rest_framework import serializers
from mturk_manager.models import Keyword

class Serializer_Keyword(serializers.ModelSerializer):

    class Meta:
        model = Keyword
        fields = (
            'id', 
            'text', 
        )
        extra_kwargs = {
            "id": {
                "read_only": False,
                # "required": False,
            },
        }