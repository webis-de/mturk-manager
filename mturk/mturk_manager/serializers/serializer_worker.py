from rest_framework import serializers
from mturk_manager.models import m_Worker
from mturk_manager.classes import Manager_Workers


# class Serializer_Worker(serializers.HyperlinkedModelSerializer):
# class Serializer_Worker(serializers.Serializer):
class Serializer_Worker(serializers.ModelSerializer):
    # is_blocked = serializers.SerializerMethodField()
    # is_blocked = serializers.JSONField(required=False)
    is_blocked_soft = serializers.BooleanField(required=False)
    is_blocked_hard = serializers.BooleanField(required=False)
    counter_assignments = serializers.IntegerField(required=False)
    # counter_assignments = serializers.JSONField(required=False)
    # is_blocked = serializers.DictField(child=serializers.IntegerField(), required=False)
    # is_blocked = serializers.IntegerField(required=False)

    class Meta:
        model = m_Worker
        fields = (
            'id', 
            'name', 
            'is_blocked_soft', 
            'is_blocked_hard', 
            'counter_assignments', 
        )
        extra_kwargs = {'name': {'required': False}}

    # def get_is_blocked(self, obj):
    #     return None

    def update(self, instance, validated_data):
        print('validated_data')
        print(validated_data)
        print('validated_data')
        dictionary_worker = Manager_Workers.update(
            database_object_project=validated_data.get('database_object_project'), 
            use_sandbox=validated_data.get('use_sandbox'), 
            name=validated_data.get('name'), 
            validated_data=validated_data
        )
        
        return dictionary_worker