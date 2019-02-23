from rest_framework import serializers
from api.models import Settings_Batch
from api.classes import Manager_Settings_Batch
from api.serializers import Serializer_Keyword, Serializer_Template_Worker
from django.db import IntegrityError


class Serializer_Settings_Batch(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(Serializer_Settings_Batch, self).__init__(*args, **kwargs)

        if 'context' in kwargs:
            if kwargs['context'].get('detailed', False):
                self.fields['template'] = Serializer_Template_Worker(source='template_worker', context=kwargs['context'])

            if kwargs['context'].get('fields'):
                allowed = set(kwargs['context'].get('fields'))
                existing = set(self.fields)
                for field_name in existing - allowed:
                    self.fields.pop(field_name)
            

    #     # print(self.fields)
    #     if foo == 3:
    #     # else:
        # self.fields['template'] = serializers.PrimaryKeyRelatedField(read_only=True)
        # self.fields['template'] = serializers.IntegerField(source='template_worker')


    keywords = Serializer_Keyword(many=True)
    qualification_locale = serializers.JSONField()

    class Meta:
        model = Settings_Batch
        fields = (
            'id', 
            'name', 
            # 'settings_batch_default',
            'title',
            'description',
            'keywords',
            'count_assignments',
            'reward',
            'lifetime',
            'duration',
            'has_content_adult',
            'qualification_assignments_approved',
            'qualification_hits_approved',
            'qualification_locale',
            'block_workers',
            'template',
            'count_assignments_max_per_worker',
        )
        extra_kwargs = {
            'name': {
                'required': False
            },
            'template': {
                'source': 'template_worker',
            },
        }


    def to_representation(self, instance):
        data = super(Serializer_Settings_Batch, self).to_representation(instance)
        import json
        try:
            data['qualification_locale'] = json.loads(data['qualification_locale'])
        except KeyError:
            # qualification_locale was excluded from the data
            pass

        return data

    def create(self, validated_data):
        print('validated_data')
        print(validated_data)
        print('validated_data')

        project = Manager_Settings_Batch.create(
            data=validated_data
        )

        return project

    def update(self, instance, validated_data):
        print('validated_data')
        print(validated_data)
        print('validated_data')

        instance = Manager_Settings_Batch.update(
            instance=instance,
            data=validated_data,
        )

        return instance