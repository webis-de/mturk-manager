from rest_framework import serializers
from mturk_manager.models import m_Hit
# from mturk_manager.classes import Manager_HITs

# class IsActiveField(serializers.Field):
#     def to_representation(self, obj):
#         return True if obj == 'Active' else False

#     def to_internal_value(self, data):
#         data = True if data == 'true' else False
#         return 'Active' if data == True else 'Inactive'

class Serializer_HIT(serializers.ModelSerializer):
# class Serializer_Batch(serializers.Serializer):
    # workers = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='mturk_manager:worker',
    #     lookup_field='name',
    # )

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
        model = m_Hit
        fields = (
            'id',
            'id_hit',
        )
        extra_kwargs = {
        }