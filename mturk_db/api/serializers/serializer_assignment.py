from rest_framework import serializers
from api.models import Assignment

# from mturk_manager.classes import Manager_HITs

# class IsActiveField(serializers.Field):
#     def to_representation(self, obj):
#         return True if obj == 'Active' else False

#     def to_internal_value(self, data):
#         data = True if data == 'true' else False
#         return 'Active' if data == True else 'Inactive'

class Serializer_Assignment(serializers.ModelSerializer):
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
    answer = serializers.JSONField()

    class Meta:
        model = Assignment
        fields = (
            'id',
            'id_assignment',
            'hit',
            'worker',
            'answer',
            'status_external',
            'status_internal',
            # 'batch',
            # 'datetime_creation',
            # 'datetime_expiration',
            # 'parameters',
            # 'count_assignments_additional',
            # 'assignments',
        )
        extra_kwargs = {
        }

    def to_representation(self, instance):
        data = super(Serializer_Assignment, self).to_representation(instance)
        import json
        data['answer'] = json.loads(data['answer'])

        return data

    # def update(self, instance, validated_data):
    #     print('validated_data')
    #     print(validated_data)
    #     print('validated_data')
    #     print(instance)

    #     instance = Manager_Assignments.update(
    #         instance=instance,
    #         data=validated_data,
    #     )

    #     return instance