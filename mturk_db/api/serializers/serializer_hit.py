from rest_framework import serializers

from api.helpers import keep_fields
from api.models import HIT
from api.serializers import Serializer_Batch


# from mturk_manager.classes import Manager_HITs

# class IsActiveField(serializers.Field):
#     def to_representation(self, obj):
#         return True if obj == 'Active' else False

#     def to_internal_value(self, data):
#         data = True if data == 'true' else False
#         return 'Active' if data == True else 'Inactive'

class Serializer_HIT(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(Serializer_HIT, self).__init__(*args, **kwargs)

        context = kwargs.get('context', {})

        if context.get('usecase') == 'list_hits':
            self.fields['batch'] = Serializer_Batch(read_only=True)

        keep_fields(self, context.get('fields'))

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
    # assignments = Serializer_Assignment(many=True, read_only=True)

    count_assignments_total = serializers.IntegerField(required=False)
    count_assignments_approved = serializers.IntegerField(required=False)
    count_assignments_rejected = serializers.IntegerField(required=False)
    count_assignments_submitted = serializers.IntegerField(required=False)
    count_assignments_dead = serializers.IntegerField(required=False)
    count_assignments_pending = serializers.IntegerField(required=False)


    class Meta:
        model = HIT
        fields = (
            'id',
            'id_hit',
            'batch',
            'datetime_creation',
            'datetime_expiration',
            'parameters',

            'count_assignments_total',
            'count_assignments_approved',
            'count_assignments_rejected',
            'count_assignments_submitted',
            'count_assignments_dead',
            'count_assignments_pending',

            # 'assignments',
        )
        extra_kwargs = {
        }