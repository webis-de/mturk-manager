from rest_framework import serializers
from mturk_manager.models import m_Batch
from mturk_manager.classes import Manager_Batches
from mturk_manager.serializers import Serializer_HIT

# class IsActiveField(serializers.Field):
#     def to_representation(self, obj):
#         return True if obj == 'Active' else False

#     def to_internal_value(self, data):
#         data = True if data == 'true' else False
#         return 'Active' if data == True else 'Inactive'

class Serializer_Batch(serializers.ModelSerializer):
# class Serializer_Batch(serializers.Serializer):
    # workers = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='mturk_manager:worker',
    #     lookup_field='name',
    # )
    settings = serializers.DictField(required=False)
    data_csv = serializers.ListField(required=False)
    # url = serializers.HyperlinkedIdentityField(view_name='mturk_manager:project_api_tmp', lookup_field='name')
    hits = Serializer_HIT(many=True, read_only=True)

    # name_database = serializers.CharField(max_length=255, required=False)
    # description_database = serializers.CharField(required=False)

    # id_mturk = serializers.CharField(max_length=255, source='QualificationTypeId', required=False)
    # created_at = serializers.DateTimeField(source='CreationTime', required=False)
    # name_mturk = serializers.CharField(max_length=255, source='Name', required=False)
    # description_mturk = serializers.CharField(source='Description', required=False)
    # keywords = serializers.CharField(source='Keywords', required=False)
    # # is_active = IsActiveField(source='QualificationTypeStatus', required=False)
    # is_requestable = serializers.NullBooleanField(source='IsRequestable', required=False)
    # is_auto_granted = serializers.NullBooleanField(source='AutoGranted', required=False)

    class Meta:
        model = m_Batch
        fields = (
            'id',
            'name',
            'title',
            'description',
            'keywords',
            'count_assignments',
            'use_sandbox',
            'reward',
            'lifetime',
            'duration',
            'fk_template',
            'hits',

            'data_csv',
            'settings',
        )
        extra_kwargs = {
            'name': {'required': False},
            'title': {'required': False},
            'description': {'required': False},
            'keywords': {'required': False},
            'count_assignments': {'required': False},
            # 'use_sandbox': {'required': False},
            'reward': {'required': False},
            'lifetime': {'required': False},
            'duration': {'required': False},
            # 'fk_template': {'required': False},
        }


    def create(self, validated_data):
        print('validated_data')
        print(validated_data)
        print('validated_data')

        batch = Manager_Batches.create(
            database_object_project=validated_data.get('database_object_project'), 
            use_sandbox=validated_data.get('use_sandbox'), 
            data=validated_data
        )

        return batch
        # return {'data_csv': []}

    def update(self, instance, validated_data):
        print('validated_data')
        print(validated_data)
        print('validated_data')

        # dictionary_qualification = Manager_Qualifications.update(
        #     database_object_project=validated_data.get('database_object_project'), 
        #     use_sandbox=validated_data.get('use_sandbox'), 
        #     id_mturk=validated_data.get('id_mturk'), 
        #     validated_data=validated_data
        # )
        
        return dictionary_qualification

    # def get_is_active(self, obj):
    #     try:
    #         return True if obj['QualificationTypeStatus'] == 'Active' else False
    #     except KeyError:
    #         return None


