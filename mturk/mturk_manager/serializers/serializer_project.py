from rest_framework import serializers
from mturk_manager.models import m_Project, m_Worker
from mturk_manager.serializers import Serializer_Worker

class Serializer_Project(serializers.ModelSerializer):
    # workers = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='mturk_manager:worker',
    #     lookup_field='name',
    # )
    # url = serializers.HyperlinkedIdentityField(view_name='mturk_manager:project_api_tmp', lookup_field='name')
    # workers = Serializer_Worker(many=True, read_only=True)

    class Meta:
        model = m_Project
        fields = (
            'id', 
            'name', 
            'slug', 
            # 'workers',
            'title',
            'description',
            'keywords',
            'count_assignments',
            'reward',
            'lifetime',
            'duration',
            'use_sandbox',
            'has_content_adult',
            'qualification_assignments_approved',
            'qualification_hits_approved',
            'qualification_locale',
            'block_workers',
        )
