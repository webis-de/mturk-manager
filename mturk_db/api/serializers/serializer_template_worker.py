from rest_framework import serializers

from api.helpers import keep_fields
from api.models import Template_Worker, Template_Assignment, Template_HIT, Template_Global
# from api.models import Project, Keyword
from api.classes import Manager_Templates_Worker
from api.serializers import Serializer_Template_Assignment, Serializer_Template_HIT, Serializer_Template_Global
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



class Serializer_Template_Worker(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(Serializer_Template_Worker, self).__init__(*args, **kwargs)

        context = kwargs.get('context', {})

        if context.get('usecase') == 'list_settings_batch':
            keep_fields(self, ['id', 'name'])
        elif context.get('usecase') == 'annotation' or context.get('usecase') == 'list_templates_worker':
            self.fields['template_assignment'] = Serializer_Template_Assignment(context=context)
            self.fields['template_hit'] = Serializer_Template_HIT(context=context)
            self.fields['template_global'] = Serializer_Template_Global(context=context)

        if context.get('fields'):
            keep_fields(self, context.get('fields'))

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
    # qualification_locale = serializers.ListField()
    # count_assignments_max_per_worker = CustomField()
    # count_assignments_max_per_worker = serializers.SerializerMethodField()

    # template_assignment = Serializer_Template_Assignment()
    # template_hit = Serializer_Template_HIT()
    # template_global = Serializer_Template_Global()


    class Meta:
        model = Template_Worker
        fields = (
            'id',
            'name',
            'height_frame',
            'template',
            'json_dict_parameters',
            'template_assignment',
            'template_hit',
            'template_global',
            # 'settings_batch_default',
            # 'title',
            # 'description',
            # 'keywords',
            # 'count_assignments',
            # 'reward',
            # 'lifetime',
            # 'duration',
            # 'has_content_adult',
            # 'qualification_assignments_approved',
            # 'qualification_hits_approved',
            # 'qualification_locale',
            # 'block_workers',
            # 'template_worker',
            # 'count_assignments_max_per_worker',
        )
        extra_kwargs = {
            'json_dict_parameters': {'required': False}
            # 'name': {'required': False},
            # 'slug': {'required': False},
            # 'version': {'required': False},
        }

    def to_internal_value(self, data):
        # find instance for given id
        if 'template_assignment' in data:
            try:
                data['template_assignment'] = Template_Assignment.objects.get(pk=data['template_assignment'])
            except Template_Assignment.DoesNotExist:
                data['template_assignment'] = None
        if 'template_hit' in data:
            try:
                data['template_hit'] = Template_HIT.objects.get(pk=data['template_hit'])
            except Template_HIT.DoesNotExist:
                data['template_hit'] = None
        if 'template_global' in data:
            try:
                data['template_global'] = Template_Global.objects.get(pk=data['template_global'])
            except Template_Global.DoesNotExist:
                data['template_global'] = None

        return data

    def create(self, validated_data):
        print('validated_data')
        print(validated_data)
        print('validated_data')

        project = Manager_Templates_Worker.create(
            data=validated_data
        )

        return project


    def update(self, instance, validated_data):
        print('validated_data')
        print(validated_data)
        print('validated_data')

        instance = Manager_Templates_Worker.update(
            instance=instance,
            data=validated_data,
        )

        return instance

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