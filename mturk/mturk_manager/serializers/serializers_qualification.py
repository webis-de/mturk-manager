# from rest_framework import serializers
# from mturk_manager.models import m_Project, m_Worker
# from mturk_manager.serializers import Serializer_Worker

# class Serializer_Qualification(serializers.HyperlinkedModelSerializer):
#     workers = serializers.HyperlinkedRelatedField(
#         many=True,
#         read_only=True,
#         view_name='mturk_manager:worker',
#         lookup_field='name',
#     )
#     url = serializers.HyperlinkedIdentityField(view_name='mturk_manager:project_api_tmp', lookup_field='name')
#     # workers = Serializer_Worker(many=True, read_only=True)

#     class Meta:
#         model = m_Project
#         fields = ('url', 'id', 'name', 'workers')