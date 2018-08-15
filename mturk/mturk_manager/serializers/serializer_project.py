from rest_framework import serializers
from mturk_manager.models import m_Project, Keyword
from mturk_manager.serializers import Serializer_Keyword
from django.db import IntegrityError

class Serializer_Project(serializers.ModelSerializer):
    # workers = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='mturk_manager:worker',
    #     lookup_field='name',
    # )
    # url = serializers.HyperlinkedIdentityField(view_name='mturk_manager:project_api_tmp', lookup_field='name')
    # workers = Serializer_Worker(many=True, read_only=True)
    keywords = Serializer_Keyword(many=True)

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

    def update(self, instance, validated_data):
        print('validated_data')
        print(validated_data)
        print('validated_data')

        for key, value in validated_data.items():
            if key == 'keywords':
                print(value)
                instance.keywords.clear()
                for keyword in value:
                    try:
                        instance.keywords.add(keyword['id'])
                    except KeyError:
                        keyword_new = Keyword.objects.create(text=keyword['text'])
                        instance.keywords.add(keyword_new)

            else:
                setattr(instance, key, value)

        instance.save()

        return instance