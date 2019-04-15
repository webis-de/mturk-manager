# from api.classes.projects import Manager_Projects
import json

from django.db.models import F, ExpressionWrapper, DurationField, QuerySet

from api.classes import Interface_Manager_Items
from api.classes.projects import Manager_Projects
from api.enums import assignments
from api.models import Assignment, Project
from rest_framework.request import Request


# # from viewer.models import m_Tag
# # from api.views import code_shared, project
# # from api.views.project import glob_prefix_name_tag_batch, glob_prefix_name_tag_worker, glob_prefix_name_tag_hit
# import uuid, json, datetime, xmltodict
# from botocore.exceptions import ClientError
# from django.db.models import F, Value, Count, Q, Sum, IntegerField, ExpressionWrapper
# from django.conf import settings as settings_django


class Manager_Assignments(Interface_Manager_Items):
    @staticmethod
    def get_all(database_object_project, request, fields=None, use_sandbox=True):
        queryset = Assignment.objects.filter(
            hit__batch__project=database_object_project,
            hit__batch__use_sandbox=use_sandbox,
        ).select_related(
            'hit', 'worker'
        )

        queryset = Manager_Assignments.filter(
            queryset=queryset,
            request=request
        )

        queryset = Manager_Assignments.annotate(queryset)

        queryset = Manager_Assignments.sort_by(
            queryset=queryset,
            request=request
        )

        if fields is not None:
            queryset = queryset.values(
                *fields
            )

        return queryset

    @staticmethod
    def filter(queryset: QuerySet, request: Request) -> QuerySet:
        list_ids = json.loads(request.query_params.get('list_ids', '[]'))

        if len(list_ids) > 0:
            queryset = Assignment.objects.filter(
                id__in=list_ids
            )

        id_batch = request.query_params.get('id_batch')
        if id_batch is not None:
            queryset = queryset.filter(hit__batch__id=id_batch)

        id_hit = request.query_params.get('id_hit')
        if id_hit is not None:
            queryset = queryset.filter(hit__id=id_hit)

        queryset = Manager_Assignments.filter_list(
            queryset=queryset,
            request=request,
            name_filter='assignmentsSelected',
            name_field='id_assignment'
        )

        queryset = Manager_Assignments.filter_list(
            queryset=queryset,
            request=request,
            name_filter='hitsSelected',
            name_field='hit__id_hit'
        )

        queryset = Manager_Assignments.filter_list(
            queryset=queryset,
            request=request,
            name_filter='batchesSelected',
            name_field='hit__batch__name'
        )

        queryset = Manager_Assignments.filter_list(
            queryset=queryset,
            request=request,
            name_filter='workersSelected',
            name_field='worker__id_worker'
        )

        queryset = Manager_Assignments.filter_boolean(
            queryset=queryset,
            request=request,
            name_filter='show_only_submitted_assignments',
            name_field='status_external__isnull'
        )

        # show_only_submitted_assignments = json.loads(request.query_params.get('show_only_submitted_assignments', 'false'))
        # if show_only_submitted_assignments == True:
        #     queryset = queryset.filter(status_external__isnull=True)

        filter_worker = request.query_params.get('worker', '')
        if filter_worker != '':
            queryset = queryset.filter(worker__id_worker__icontains=filter_worker)

        return queryset

    @staticmethod
    def annotate(queryset: QuerySet) -> QuerySet:
        return queryset.annotate(
            duration=ExpressionWrapper(F('datetime_submit') - F('datetime_accept'), output_field=DurationField())
        )

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