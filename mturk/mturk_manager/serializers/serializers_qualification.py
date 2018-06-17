from rest_framework import serializers
from mturk_manager.models import Model_Qualification
# from mturk_manager.serializers import Serializer_Worker

class Serializer_Qualification(serializers.ModelSerializer):
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

    id_mturk = serializers.CharField(max_length=255, source='QualificationTypeId')
    created_at = serializers.DateTimeField(source='CreationTime')
    name_mturk = serializers.CharField(max_length=255, source='Name')
    description_mturk = serializers.CharField(source='Description')
    keywords = serializers.CharField(source='Keywords', required=False)
    is_active = serializers.SerializerMethodField()
    is_requestable = serializers.BooleanField(source='IsRequestable')
    is_auto_granted = serializers.BooleanField(source='AutoGranted')

    class Meta:
        model = Model_Qualification
        fields = (
            'id_mturk',
            'created_at',
            'name_mturk',
            'description_mturk',
            'name_database',
            'description_database',
            'keywords',
            'is_active',
            'is_requestable',
            'is_auto_granted',
        )

    def get_is_active(self, obj):
        return True if obj['QualificationTypeStatus'] == 'Active' else False