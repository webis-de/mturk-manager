from rest_framework import serializers
from mturk_manager.models import m_Worker
from mturk_manager.classes import Manager_Workers


# class Serializer_Worker(serializers.HyperlinkedModelSerializer):
class Serializer_Worker(serializers.ModelSerializer):
    class Meta:
        model = m_Worker
        fields = (
            'id', 
            'name', 
            'is_blocked',
        )
        extra_kwargs = {'name': {'required': False}}

    def update(self, instance, validated_data):
        # print('validated_data')
        # print(validated_data)
        # print('validated_data')
        dictionary_worker = Manager_Workers.update(
            database_object_project=validated_data.get('database_object_project'), 
            use_sandbox=validated_data.get('use_sandbox'), 
            name=validated_data.get('name'), 
            validated_data=validated_data
        )
        
        return dictionary_worker