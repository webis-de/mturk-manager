from rest_framework import serializers
from api.models import Worker
from api.classes import Manager_Workers

# from mturk_manager.classes import Manager_HITs

# class IsActiveField(serializers.Field):
#     def to_representation(self, obj):
#         return True if obj == 'Active' else False

#     def to_internal_value(self, data):
#         data = True if data == 'true' else False
#         return 'Active' if data == True else 'Inactive'

class Serializer_Worker(serializers.ModelSerializer):
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
    # answer = serializers.JSONField()
    is_blocked_hard = serializers.BooleanField(required=False)
    is_blocked_soft = serializers.BooleanField(required=False)
    count_assignments_limit = serializers.IntegerField(required=False)
    number_of_assignments = serializers.IntegerField(required=False)

    number_of_approved_assignments = serializers.IntegerField(required=False)
    number_of_rejected_assignments = serializers.IntegerField(required=False)
    ratio_approved_assignments = serializers.FloatField(required=False)
    number_of_approved_assignments_of_project = serializers.IntegerField(required=False)
    number_of_rejected_assignments_of_project = serializers.IntegerField(required=False)
    ratio_approved_assignments_of_project = serializers.FloatField(required=False)

    class Meta:
        model = Worker
        fields = (
            'id',
            'id_worker',
            'is_blocked_hard',
            'is_blocked_soft',
            'is_blocked_global',
            'count_assignments_limit',
            'number_of_assignments',

            'number_of_approved_assignments',
            'number_of_rejected_assignments',
            'ratio_approved_assignments',
            'number_of_approved_assignments_of_project',
            'number_of_rejected_assignments_of_project',
            'ratio_approved_assignments_of_project',
            # 'project',
            # 'hit',
            # 'worker',
            # 'answer',
            # 'id_hit',
            # 'batch',
            # 'datetime_creation',
            # 'datetime_expiration',
            # 'parameters',
            # 'count_assignments_additional',
            # 'assignments',
        )
        extra_kwargs = {
            # 'is_blocked_hard': {'required': False}
        }

    # def to_representation(self, instance):
    #     data = super(Serializer_Assignment, self).to_representation(instance)
    #     import json
    #     data['answer'] = json.loads(data['answer'])

    #     return data

    def update(self, instance, validated_data):
        print('validated_data')
        print(validated_data)
        print('validated_data')
        dictionary_worker = Manager_Workers.update(
            data=validated_data,
            instance=instance,
        )
        
        return dictionary_worker