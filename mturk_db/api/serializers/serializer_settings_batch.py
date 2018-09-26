from rest_framework import serializers
from api.models import Settings_Batch
# from api.models import Project, Keyword
from api.classes import Manager_Settings_Batch
from api.serializers import Serializer_Keyword
from django.db import IntegrityError

# class CustomField(serializers.Field):
#     def get_attribute(self, obj):
#         return obj

#     def to_representation(self, obj):
#         response = Manager_Global_DB.get_count_assignments_max_per_worker(obj.slug)
#         return response

#     # def get_value(self, obj):
#         # return obj

#     def to_internal_value(self, data):
#         # print('++++++')
#         # print(data)
#         # response = Manager_Global_DB.set_count_assignments_max_per_worker(obj.slug, data)
#         return int(data)



class Serializer_Settings_Batch(serializers.ModelSerializer):
    # workers = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='mturk_manager:worker',
    #     lookup_field='name',
    # )
    # url = serializers.HyperlinkedIdentityField(view_name='mturk_manager:project_api_tmp', lookup_field='name')
    # workers = Serializer_Worker(many=True, read_only=True)
    keywords = Serializer_Keyword(many=True)
    # templates = Serializer_Template_Worker(many=True)
    qualification_locale = serializers.JSONField()
    # qualification_locale = serializers.ListField()
    # count_assignments_max_per_worker = CustomField()
    # count_assignments_max_per_worker = serializers.SerializerMethodField()


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
            'template': {
                'source': 'template_worker',
            },
            # 'slug': {'required': False},
            # 'version': {'required': False},
        }


    def to_representation(self, instance):
        data = super(Serializer_Settings_Batch, self).to_representation(instance)
        import json
        data['qualification_locale'] = json.loads(data['qualification_locale'])

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


    # def get_count_assignments_max_per_worker(self, obj):
    #     response = Manager_Global_DB.get_count_assignments_max_per_worker(obj.slug)
    #     return response