from rest_framework import serializers
from api.models import Batch, Settings_Batch, Project
from api.classes import Manager_Batches
from api.serializers import Serializer_Settings_Batch, Serializer_Keyword, Serializer_Template_Worker

# class IsActiveField(serializers.Field):
#     def to_representation(self, obj):
#         return True if obj == 'Active' else False

#     def to_internal_value(self, data):
#         data = True if data == 'true' else False
#         return 'Active' if data == True else 'Inactive'

class Serializer_Batch(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(Serializer_Batch, self).__init__(*args, **kwargs)

        context = kwargs.get('context', {})

        self.fields['settings_batch'] = Serializer_Settings_Batch(context=context)

    settings_batch = Serializer_Settings_Batch()

    data_csv = serializers.ListField(required=False)
    # hits = Serializer_HIT(many=True, read_only=True)
    count_hits = serializers.IntegerField(required=False)

    count_assignments_total = serializers.IntegerField(required=False)
    count_assignments_approved = serializers.IntegerField(required=False)
    count_assignments_rejected = serializers.IntegerField(required=False)
    count_assignments_submitted = serializers.IntegerField(required=False)
    count_assignments_dead = serializers.IntegerField(required=False)
    count_assignments_pending = serializers.IntegerField(required=False)

    count_assignments_available = serializers.IntegerField(required=False)

    costs_max = serializers.IntegerField(required=False)
    costs_so_far = serializers.IntegerField(required=False)

    class Meta:
        model = Batch
        fields = (
            'id', 
            'name',
            'count_hits',
            'datetime_creation',
            'project',
            'use_sandbox',
            # 'hits',
            'data_csv',
            'settings_batch',

            'count_assignments_total',
            'count_assignments_approved',
            'count_assignments_rejected',
            'count_assignments_submitted',
            'count_assignments_dead',
            'count_assignments_pending',

            'count_assignments_available',

            'costs_max',
            'costs_so_far',
        )
        extra_kwargs = {
            # 'template': {
            #     'source': 'template_worker',
            # },
            'name': {'required': False},
            'use_sandbox': {'required': False},
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

        batch = Batch.objects.get_or_create(name='gmudupzvxtjtpmcepnre', use_sandbox=True)[0]
        foo = Settings_Batch.objects.get_or_create(name='gmudupzvxtjtpmcepnre', defaults={
            'batch': batch,
            'project': Project.objects.first()
        })

        print(foo)

        return batch
        # return batch
        # return {'data_csv': []}

    def update(self, instance, validated_data):
        print('validated_data')
        print(validated_data)
        print('validated_data')

        return dictionary_qualification

