from rest_framework import serializers
from api.models import Project
# from api.models import Project, Keyword
from api.classes import Manager_Projects
# from mturk_manager.serializers import Serializer_Keyword, Serializer_Template_Worker
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



class Serializer_Project(serializers.ModelSerializer):
    # workers = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='mturk_manager:worker',
    #     lookup_field='name',
    # )
    # url = serializers.HyperlinkedIdentityField(view_name='mturk_manager:project_api_tmp', lookup_field='name')
    # workers = Serializer_Worker(many=True, read_only=True)
    # keywords = Serializer_Keyword(many=True)
    # templates = Serializer_Template_Worker(many=True)

    # count_assignments_max_per_worker = CustomField()
    # count_assignments_max_per_worker = serializers.SerializerMethodField()


    class Meta:
        model = Project
        fields = (
            'id', 
            'name', 
            'slug', 
            'version',
            'settings_batch_default',
            'count_assignments_max_per_worker',
            # 'workers',
            # 'title',
            # 'description',
            # 'keywords',
            # 'count_assignments',
            # 'reward',
            # 'lifetime',
            # 'duration',
            # 'use_sandbox',
            # 'has_content_adult',
            # 'qualification_assignments_approved',
            # 'qualification_hits_approved',
            # 'qualification_locale',
            # 'block_workers',
            # 'templates',
            # 'fk_template_main',
            # 'count_assignments_max_per_worker',
        )
        extra_kwargs = {
            # 'name': {'required': False},
            'slug': {'required': False},
            'version': {'required': False},
        }

    def create(self, validated_data):
        print('validated_data')
        print(validated_data)
        print('validated_data')

        project = Manager_Projects.create(
            data=validated_data
        )

        return project

    # def update(self, instance, validated_data):
    #     print('validated_data')
    #     print(validated_data)
    #     print('validated_data')

    #     for key, value in validated_data.items():
    #         if key == 'keywords':
    #             print(value)
    #             instance.keywords.clear()
    #             for keyword in value:
    #                 try:
    #                     instance.keywords.add(keyword['id'])
    #                 except KeyError:
    #                     keyword_new = Keyword.objects.get_or_create(text=keyword['text'])[0]
    #                     instance.keywords.add(keyword_new)
    #         elif key == 'count_assignments_max_per_worker':
    #             response = Manager_Global_DB.set_count_assignments_max_per_worker(instance.slug, value)

    #         else:
    #             print('key')
    #             print(key)
    #             print(value)
    #             setattr(instance, key, value)

    #     instance.save()

    #     return instance


    # def get_count_assignments_max_per_worker(self, obj):
    #     response = Manager_Global_DB.get_count_assignments_max_per_worker(obj.slug)
    #     return response