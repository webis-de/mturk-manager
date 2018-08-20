from rest_framework import serializers
from mturk_manager.models import Model_Qualification
from mturk_manager.classes import Manager_Qualifications

# class IsActiveField(serializers.Field):
#     def to_representation(self, obj):
#         return True if obj == 'Active' else False

#     def to_internal_value(self, data):
#         data = True if data == 'true' else False
#         return 'Active' if data == True else 'Inactive'

class Serializer_Qualification(serializers.Serializer):
    # workers = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='mturk_manager:worker',
    #     lookup_field='name',
    # )
    # url = serializers.HyperlinkedIdentityField(view_name='mturk_manager:project_api_tmp', lookup_field='name')
    # workers = Serializer_Worker(many=True, read_only=True)

    name_database = serializers.CharField(max_length=255, required=False)
    description_database = serializers.CharField(required=False)

    id_mturk = serializers.CharField(max_length=255, source='QualificationTypeId', required=False)
    created_at = serializers.DateTimeField(source='CreationTime', required=False)
    name_mturk = serializers.CharField(max_length=255, source='Name', required=False)
    description_mturk = serializers.CharField(source='Description', required=False)
    keywords = serializers.CharField(source='Keywords', required=False)
    # is_active = IsActiveField(source='QualificationTypeStatus', required=False)
    is_requestable = serializers.NullBooleanField(source='IsRequestable', required=False)
    is_auto_granted = serializers.NullBooleanField(source='AutoGranted', required=False)

    # class Meta:
    #     model = Model_Qualification
    #     fields = (
    #         'id_mturk',
    #         'created_at',
    #         'name_mturk',
    #         'description_mturk',
    #         'name_database',
    #         'description_database',
    #         'keywords',
    #         'is_active',
    #         'is_requestable',
    #         'is_auto_granted',
    #     )

    def create(self, validated_data):
        print('validated_data')
        print(validated_data)
        print('validated_data')

        dictionary_qualification = Manager_Qualifications.create(
            database_object_project=validated_data.get('database_object_project'), 
            use_sandbox=validated_data.get('use_sandbox'), 
            validated_data=validated_data
        )

        return dictionary_qualification

    def update(self, instance, validated_data):
        print('validated_data')
        print(validated_data)
        print('validated_data')
        dictionary_qualification = Manager_Qualifications.update(
            database_object_project=validated_data.get('database_object_project'), 
            use_sandbox=validated_data.get('use_sandbox'), 
            id_mturk=validated_data.get('id_mturk'), 
            validated_data=validated_data
        )
        
        return dictionary_qualification

    # def get_is_active(self, obj):
    #     try:
    #         return True if obj['QualificationTypeStatus'] == 'Active' else False
    #     except KeyError:
    #         return None


