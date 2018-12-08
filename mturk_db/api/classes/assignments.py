# from api.classes.projects import Manager_Projects
import json

from api.enums import assignments
from api.classes.projects import Manager_Projects
from api.models import Assignment

# # from viewer.models import m_Tag
# # from api.views import code_shared, project
# # from api.views.project import glob_prefix_name_tag_batch, glob_prefix_name_tag_worker, glob_prefix_name_tag_hit
# import uuid, json, datetime, xmltodict
# from botocore.exceptions import ClientError
# from django.db.models import F, Value, Count, Q, Sum, IntegerField, ExpressionWrapper
# from django.conf import settings as settings_django

class Manager_Assignments(object):
    @staticmethod
    def get(database_object_project, use_sandbox, request):
        queryset = Assignment.objects.filter(
            hit__batch__project=database_object_project,
            hit__batch__use_sandbox=use_sandbox,
        )

        id_batch = request.query_params.get('id_batch')
        if id_batch is not None:
            queryset = queryset.filter(hit__batch__id=id_batch)

        id_hit = request.query_params.get('id_hit')
        if id_hit is not None:
            queryset = queryset.filter(hit__id=id_hit)

        show_only_submitted_assignments = json.loads(request.query_params.get('show_only_submitted_assignments', 'false'))
        if show_only_submitted_assignments == True:
            queryset = queryset.filter(status_external__isnull=True)

        filter_worker = request.query_params.get('worker', '')
        if filter_worker != '':
            queryset = queryset.filter(worker__id_worker__icontains=filter_worker)

        queryset = queryset.annotate(
        )

        sort_by = request.query_params.get('sort_by')
        if sort_by is not None:
            descending = request.query_params.get('descending', 'false') == 'true'
            queryset = queryset.order_by(
                ('-' if descending else '') + sort_by
            )

        return queryset

    @classmethod
    def get_all(cls, database_object_project, list_ids, use_sandbox=True):
        # import time
        # time.sleep(2)
        if len(list_ids) > 0:
            queryset_batch = Assignment.objects.filter(
                hit__batch__project=database_object_project, 
                id__in=list_ids
            )
        else:
            queryset_batch = Assignment.objects.filter(hit__batch__project=database_object_project)
        return queryset_batch

    @staticmethod
    def update_stati_assignments(database_object_project, data):
        object_assignments = data['assignments']
        message_reject_default = data['message_reject_default']

        client_sandbox = Manager_Projects.get_mturk_api(True)
        client_real = Manager_Projects.get_mturk_api(False)

        list_ids_assignment = list(object_assignments.keys())

        queryset_assignments = Assignment.objects.filter(
            id__in=list_ids_assignment
        ).select_related('hit__batch')
        for assignment in queryset_assignments:
            object_assignment = object_assignments[str(assignment.id)]
            state = object_assignment['state']
            # message = object_assignments[str(assignment.id)].get('message')
            print(state)
            # print(message)

            if state == 'approve':
                assignment.status_external = assignments.STATUS_EXTERNAL.APPROVED
                assignment.status_internal = None
            elif state == 'reject':
                assignment.status_external = assignments.STATUS_EXTERNAL.REJECTED
                assignment.status_internal = None
            elif state == 'approve_internally':
                assignment.status_external = assignments.STATUS_EXTERNAL.REJECTED
                assignment.status_internal = assignments.STATUS_INTERNAL.APPROVED
            elif state == 'reject_internally':
                assignment.status_external = assignments.STATUS_EXTERNAL.APPROVED
                assignment.status_internal = assignments.STATUS_INTERNAL.REJECTED

            client = client_sandbox if assignment.hit.batch.use_sandbox == True else client_real


            if assignment.status_external == assignments.STATUS_EXTERNAL.APPROVED:
                response = client.approve_assignment(
                    AssignmentId=assignment.id_assignment,
                    # RequesterFeedback=feedback
                )
            elif assignment.status_external == assignments.STATUS_EXTERNAL.REJECTED:
                feedback = object_assignment.get('message', message_reject_default)
                response = client.reject_assignment(
                    AssignmentId=assignment.id_assignment,
                    RequesterFeedback=feedback
                )

            assignment.save()