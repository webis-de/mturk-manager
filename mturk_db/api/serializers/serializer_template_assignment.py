from rest_framework import serializers

from api.classes import Manager_Templates_Assignment
from api.helpers import keep_fields
from api.models import Template_Assignment


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



class Serializer_Template_Assignment(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(Serializer_Template_Assignment, self).__init__(*args, **kwargs)

        context = kwargs.get('context', {})

        if context.get('usecase') == 'list_templates_worker':
            keep_fields(
                serializer=self,
                fields=['id', 'name']
            )

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
    # templates = Serializer_Template_Assignment(many=True)
    # qualification_locale = serializers.ListField()
    # count_assignments_max_per_worker = CustomField()
    # count_assignments_max_per_worker = serializers.SerializerMethodField()


    class Meta:
        model = Template_Assignment
        fields = (
            'id', 
            'name', 
            'template', 
        )
        extra_kwargs = {
        }

    def create(self, validated_data):
        print('validated_data')
        print(validated_data)
        print('validated_data')

        project = Manager_Templates_Assignment.create(
            data=validated_data
        )

        return project

    def update(self, instance, validated_data):
        print('validated_data')
        print(validated_data)
        print('validated_data')

        instance = Manager_Templates_Assignment.update(
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