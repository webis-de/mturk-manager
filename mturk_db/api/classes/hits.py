# from api.classes.projects import Manager_Projects
from api.models import HIT
# # from viewer.models import m_Tag
# # from api.views import code_shared, project
# # from api.views.project import glob_prefix_name_tag_batch, glob_prefix_name_tag_worker, glob_prefix_name_tag_hit
# import uuid, json, datetime, xmltodict
# from botocore.exceptions import ClientError
# from django.db.models import F, Value, Count, Q, Sum, IntegerField, ExpressionWrapper
# from django.conf import settings as settings_django

class Manager_HITs(object):
    @classmethod
    def get_all(cls, database_object_project, list_ids, use_sandbox=True):
        # import time
        # time.sleep(2)
        if len(list_ids) > 0:
            queryset_batch = HIT.objects.filter(
                batch__project=database_object_project, 
                id__in=list_ids
            )
        else:
            queryset_batch = HIT.objects.filter(batch__project=database_object_project)
        return queryset_batch