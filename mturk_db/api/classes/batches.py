import collections
import csv
import json
import uuid
import xmltodict

from botocore.exceptions import ClientError
from django.conf import settings as settings_django
from django.db.models import F, Count, Q, QuerySet, Case, When, BooleanField, IntegerField, ExpressionWrapper, Subquery, \
    OuterRef, Sum
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from rest_framework.request import Request
from django.utils import timezone

from api.classes import Interface_Manager_Items
from api.classes.projects import Manager_Projects
from api.enums import assignments, STATUS_EXTERNAL, STATUS_INTERNAL
from api.models import Batch, HIT, Assignment, Settings_Batch, Worker
from api.helpers import mturk_status_to_database_status

class Manager_Batches(Interface_Manager_Items):
    @staticmethod
    def get_all(database_object_project, request, fields=None, use_sandbox=None):
        queryset = Batch.objects.filter(
            project=database_object_project,
            use_sandbox=use_sandbox,
        )

        queryset = Manager_Batches.filter(
            queryset=queryset,
            request=request
        )

        queryset = Manager_Batches.annotate(queryset)

        queryset = Manager_Batches.sort_by(
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
            queryset = Batch.objects.filter(
                id__in=list_ids
            )

        queryset = Manager_Batches.filter_list(
            queryset=queryset,
            request=request,
            name_filter='batchesSelected',
            name_field='name'
        )

        return queryset

    @staticmethod
    def annotate(queryset: QuerySet) -> QuerySet:
        now = timezone.now()

        foo = HIT.objects.filter(batch=OuterRef('id'), datetime_expiration__gt=now).values('batch').annotate(
            count_assignments=Coalesce(Count(
                'assignments',
                distinct=True,
            ), 0)
        ).values('count_assignments')

        bar = HIT.objects.filter(batch=OuterRef('id'), datetime_expiration__gt=now).values('batch').annotate(
            count_assignments=Coalesce(Sum(
                'batch__settings_batch__count_assignments',
                distinct=True,
            ), 0)
        ).values('count_assignments')

        return queryset.annotate(
            count_hits=Count('hits', distinct=True)
        ).annotate(
            count_assignments_total=F('count_hits') * F('settings_batch__count_assignments'),
            count_assignments_approved=Coalesce(Count(
                'hits__assignments',
                distinct=True,
                filter=Q(hits__assignments__status_external=assignments.STATUS_EXTERNAL.APPROVED)
            ), 0),
            count_assignments_rejected=Coalesce(Count(
                'hits__assignments',
                distinct=True,
                filter=Q(hits__assignments__status_external=assignments.STATUS_EXTERNAL.REJECTED)
            ), 0),
            count_assignments_submitted=Coalesce(Count(
                'hits__assignments',
                distinct=True,
                filter=Q(hits__assignments__status_external__isnull=True)
            ), 0),
            count_assignments_dead=Coalesce(Sum(
                'hits__count_assignments_dead',
                distinct=True
            ), 0),
            count_assignments_living_total=Coalesce(Subquery(
                bar,
                output_field=IntegerField()
            ), 0),
            count_assignments_living_available=Coalesce(Subquery(
                foo,
                output_field=IntegerField()
            ), 0),
            # TODO can be deleted?
            count_assignments_available=Coalesce(Count('hits__assignments', distinct=True), 0),
        ).annotate(
            count_assignments_pending=F('count_assignments_living_total') - F('count_assignments_living_available'),
            costs_max=F('count_assignments_total') * F('settings_batch__reward'),
            costs_so_far=F('count_assignments_approved') * F('settings_batch__reward'),
        )

    @staticmethod
    def get(id_batch):
        batch = Batch.objects.get(
            pk=id_batch
        )

        return batch

    @staticmethod
    def create(data, database_object_project=None, use_sandbox=True):

        client = Manager_Projects.get_mturk_api(use_sandbox)
        # client = Manager_Projects.get_mturk_api(database_object_project, use_sandbox)
        dictionary_settings_batch = data['settings_batch']

        # print('+++++++++++++++++++++++++++')
        # print(dictionary_settings_batch)
        # print(dictionary_settings_batch['keywords'])
        # print(dictionary_settings_batch['assignments_max'])
        # print(dictionary_settings_batch['lifetime'])
        # print(dictionary_settings_batch['duration'])
        # print(dictionary_settings_batch['reward'])
        # print(dictionary_settings_batch['title'])
        # print(dictionary_settings_batch['description'])
        # print(dictionary_settings_batch['template'])
        # print('missing: AutoApprovalDelayInSeconds, Question, QualificationRequirement')
        # print('+++++++++++++++++++++++++++')

        if dictionary_settings_batch['block_workers']:
            dictionary_settings_batch['template_worker'].template = Manager_Batches.preprocess_template_request(database_object_project, dictionary_settings_batch['template_worker'].template)

        # print(data['template_worker'].template)
        try:
            name_batch = data['name'].upper()
        except KeyError:
            name_batch = uuid.uuid4().hex.upper()

        database_object_batch = Batch.objects.create(
            name=name_batch,
            project=database_object_project,
            use_sandbox=use_sandbox,
        )

        settings_batch = Settings_Batch.objects.create(
            batch=database_object_batch,
            project=database_object_project,
            name='{}__{}__{}'.format(database_object_project.id, name_batch, uuid.uuid4().hex),

            title=dictionary_settings_batch.get('title'),
            reward=dictionary_settings_batch.get('reward'),
            count_assignments=dictionary_settings_batch.get('count_assignments'),
            count_assignments_max_per_worker=dictionary_settings_batch.get('count_assignments_max_per_worker'),
            description=dictionary_settings_batch.get('description'),
            lifetime=dictionary_settings_batch.get('lifetime'),
            duration=dictionary_settings_batch.get('duration'),
            block_workers=dictionary_settings_batch.get('block_workers'),
            template_worker=dictionary_settings_batch.get('template_worker'),

            has_content_adult=dictionary_settings_batch.get('has_content_adult'),
            qualification_assignments_approved=dictionary_settings_batch.get('qualification_assignments_approved'),
            qualification_hits_approved=dictionary_settings_batch.get('qualification_hits_approved'),
            qualification_locale=json.dumps(dictionary_settings_batch.get('qualification_locale')),

        )
        settings_batch.keywords.set([keyword['id'] for keyword in dictionary_settings_batch['keywords']])
        settings_batch.save()

        title = dictionary_settings_batch['title']
        if dictionary_settings_batch['has_content_adult'] == True:
            title = 'Contains adult content! {}'.format(title)


        # return database_object_batch
        for index, dictionary_hit in enumerate(data['data_csv']):
            try:
                mturk_obj_hit = client.create_hit(
                    Keywords=','.join([keyword['text'] for keyword in dictionary_settings_batch['keywords']]),
                    MaxAssignments=dictionary_settings_batch['count_assignments'],
                    LifetimeInSeconds=dictionary_settings_batch['lifetime'],
                    AssignmentDurationInSeconds=dictionary_settings_batch['duration'],
                    AutoApprovalDelayInSeconds=1209600,
                    Reward=Manager_Batches.cent_to_dollar(dictionary_settings_batch['reward']),
                    Title=title,
                    Description=dictionary_settings_batch['description'],
                    Question=Manager_Batches.create_question(dictionary_settings_batch['template_worker'].template, dictionary_settings_batch['template_worker'].height_frame, dictionary_hit),
                    QualificationRequirements=[]
                    # QualificationRequirements=Manager_Batches.get_qualifications(data)
                )
                pass
            except ClientError as e:
                print(e)
                # messages.error(request, '''
                #     An error occured
                #     <a href="#alert_1" data-toggle="collapse" class="alert-link">details</a>
                #     <p class="collapse mb-0" id="alert_1">
                #         {}
                #     </p>
                # '''.format(e))

                if index == 0:
                    database_object_batch.delete()

                break

            # db_obj_tag = m_Tag.objects.create(
            #     name=project.glob_prefix_name_tag_hit+mturk_obj_hit['HIT']['HITId'],
            #     key_corpus=database_object_project.name
            # )

            # print(mturk_obj_hit)
            db_obj_hit = HIT.objects.create(
                # id_hit=str(random.randint(0, 9999999)),
                id_hit=mturk_obj_hit['HIT']['HITId'].upper(),
                batch=database_object_batch,
                parameters=json.dumps(dictionary_hit),
                datetime_expiration=mturk_obj_hit['HIT']['Expiration'],
                datetime_creation=mturk_obj_hit['HIT']['CreationTime'],
            )
            # db_obj_hit = HIT.objects.create(
            #     # id_hit=str(random.randint(0, 9999999)),
            #     id_hit=uuid.uuid4().hex,
            #     batch=database_object_batch,
            #     parameters=json.dumps(dictionary_hit),
            #     datetime_expiration=datetime.datetime.now(),
            #     datetime_creation=datetime.datetime.now(),
            # )

        # db_obj_tag = m_Tag.objects.get_or_create(
        #     name=project.glob_prefix_name_tag_batch+database_object_batch.name,
        #     key_corpus=database_object_project.name
        # )[0]
    #     for index_reader, dict_parameters in enumerate(reader):
    #     # print(index_reader)
    #     # print(len(dict_parameters))
    #     # print(dict_parameters)
    #     try:
    #         mturk_obj_hit = client.create_hit(
    #             Keywords='',
    #             # Keywords=dictionary_settings_batch['keywords'],
    #             MaxAssignments=form.cleaned_data['count_assignments'],
    #             LifetimeInSeconds=form.cleaned_data['lifetime'],
    #             AssignmentDurationInSeconds=form.cleaned_data['duration'],
    #             AutoApprovalDelayInSeconds=1209600,
    #             Reward=form.cleaned_data['reward'],
    #             Title=title,
    #             Description=form.cleaned_data['description'],
    #             Question=code_shared.create_question(db_obj_template.template, db_obj_template.height_frame, dict_parameters),
    #             QualificationRequirements=list_requirements
    #         )
    #         # print(mturk_obj_hit)
    #     except ClientError as e:
    #         messages.error(request, '''
    #             An error occured
    #             <a href="#alert_1" data-toggle="collapse" class="alert-link">details</a>
    #             <p class="collapse mb-0" id="alert_1">
    #                 {}
    #             </p>
    #         '''.format(e))

    #         if index == 0:
    #             db_obj_batch.delete()

    #         break

    #     index += 1

    #     db_obj_tag = m_Tag.objects.create(
    #         name=glob_prefix_name_tag_hit+mturk_obj_hit['HIT']['HITId'],
    #         key_corpus=db_obj_project.name
    #     )

    #     # print(mturk_obj_hit)
    #     db_obj_hit = m_Hit.objects.create(
    #         # id_hit=str(random.randint(0, 9999999)),
    #         id_hit=mturk_obj_hit['HIT']['HITId'],
    #         fk_batch=db_obj_batch,
    #         parameters=json.dumps(dict_parameters),
    #         datetime_expiration=mturk_obj_hit['HIT']['Expiration'],
    #         datetime_creation=mturk_obj_hit['HIT']['CreationTime'],
    #     )

    #     # list_assignments

    #     # list_entities.append(db_obj_hit.id)

    # db_obj_tag = m_Tag.objects.get_or_create(
    #     name=glob_prefix_name_tag_batch+db_obj_batch.name,
    #     key_corpus=db_obj_project.name
    # )[0]
        return database_object_batch

    @staticmethod
    def cent_to_dollar(amount):
        cents = amount % 100
        dollars = (amount - cents) / 100

        result = ''
        if cents <= 9:
            result = '0{}'.format(cents)
        else:
            result = '{}'.format(cents)

        return '{}.{}'.format(int(dollars), result)

    @staticmethod
    def create_question(template, height_frame, dict_parameters):
        for key, value in dict_parameters.items():
            # print('####')
            # print(key)
            # print(value)
            template = template.replace('${'+key+'}', value)

        return '''
            <HTMLQuestion xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2011-11-11/HTMLQuestion.xsd">
                <HTMLContent><![CDATA['''+template+''']]></HTMLContent>
                <FrameHeight>'''+str(height_frame)+'''</FrameHeight>
            </HTMLQuestion>'''

    @classmethod
    def preprocess_template_request(cls, db_obj_project, html_template):
        url_status_block = cls.get_url_block_worker(db_obj_project)
        url_add_counter = cls.get_url_add_counter(db_obj_project)
        # path = reverse('mturk_manager:api_status_worker', kwargs={'name':db_obj_project.name, 'id_worker':'a'})[:-1]
        # url = urllib.parse.urljoin(host, path)
        injected = ''
        injected += '''
            <script>
                var rkreu = '{url_status_block}';
                var foo = '{url_add_counter}';
                {code_block}
            </script>
        '''.format(
            url_status_block=url_status_block,
            url_add_counter=url_add_counter,
            code_block=cls.get_code_block_request(),
        )

        html_template = html_template.replace('</head>', '{}</head>'.format(injected))
        return html_template


    @classmethod
    def get_url_block_worker(cls, db_obj_project):
        url = settings_django.URL_GLOBAL_DB + '/projects/{}/workers/status_block/'.format(db_obj_project.slug)

        if url.startswith('http'):
            url = url.replace('http://', 'https://')
        else:
            url = 'https://' + url

        return url

    @classmethod
    def get_url_add_counter(cls, db_obj_project):
        url = settings_django.URL_GLOBAL_DB + '/projects/{}/workers/increment_counter'.format(db_obj_project.slug)

        if url.startswith('http'):
            url = url.replace('http://', 'https://')
        else:
            url = 'https://' + url

        return url

    @classmethod
    def get_code_block_request(cls):
        return "'use strict';function request(a,b,c){var d=3<arguments.length&&arguments[3]!==void 0?arguments[3]:void 0,f=void 0;window.XMLHttpRequest?f=new XMLHttpRequest:window.ActiveXObject&&(f=new ActiveXObject('Microsoft.XMLHTTP')),f.open(b,a,!0),f.setRequestHeader('Authorization','Token 5f1b3a6798667142f158364b3c1ea73b029c04e2'),f.setRequestHeader('Content-Type','application/json'),f.onreadystatechange=function(){try{4===f.readyState&&200===f.status&&c(f)}catch(h){}},d==void 0?f.send():f.send(JSON.stringify(d))}function rkreuFunc(a){var b=turkGetParam('workerId');if(void 0!=b&&''!=b){var c=a+b+'?'+new Date().getTime();request(c,'GET',function(d){!0==JSON.parse(d.responseText).is_blocked?document.body.innerHTML='<h1>Temporary limit reached. Please return this HIT.</h1><p>We decided for this procedure, so we don&#39;t have to reject many HITs and affect your ratings.</p><p>Thank you.</p>':add_counter()})}}function turkGetParam(a){var c=new RegExp('[?&]'+a+'=([^&#]*)'),d=window.location.href,f=c.exec(d);return null==f?'':f[1]}rkreuFunc(rkreu);function add_counter(){var a={id_assignment:turkGetParam('assignmentId'),id_worker:turkGetParam('workerId')};request(foo,'POST',function(){},a)}"


    # @classmethod
    # def get_qualifications(cls, dictionary_settings_batch):
    #     list_requirements = []

    #     if dictionary_settings_batch['qualification_locale'] and len(dictionary_settings_batch) > 0:
    #         list_requirements.append({
    #             'QualificationTypeId': '00000000000000000071',
    #             'Comparator': 'In',
    #             'LocaleValues': [{'Country': locale.strip().upper()} for locale in dictionary_settings_batch['qualification_locale']],
    #             'RequiredToPreview': True
    #             # 'ActionsGuarded': 'PreviewAndAccept'
    #         })
    #     if dictionary_settings_batch['qualification_assignments_approved']:
    #         list_requirements.append({
    #             'QualificationTypeId': '000000000000000000L0',
    #             'Comparator': 'GreaterThanOrEqualTo',
    #             'IntegerValues': [
    #                 dictionary_settings_batch['qualification_assignments_approved'],
    #             ],
    #             'RequiredToPreview': True
    #             # 'ActionsGuarded': 'PreviewAndAccept'
    #         })
    #     if dictionary_settings_batch['qualification_hits_approved']:
    #         list_requirements.append({
    #             'QualificationTypeId': '00000000000000000040',
    #             'Comparator': 'GreaterThanOrEqualTo',
    #             'IntegerValues': [
    #                 dictionary_settings_batch['qualification_hits_approved'],
    #             ],
    #             'RequiredToPreview': True
    #             # 'ActionsGuarded': 'PreviewAndAccept'
    #         })
    #     if dictionary_settings_batch['has_content_adult']:
    #         list_requirements.append({
    #             'QualificationTypeId': '00000000000000000060',
    #             'Comparator': 'EqualTo',
    #             'IntegerValues': [
    #                 1,
    #             ],
    #             'RequiredToPreview': True
    #             # 'ActionsGuarded': 'PreviewAndAccept'
    #         })

    #     return list_requirements

    @staticmethod
    def sync_mturk(database_object_project, use_sandbox):
        # fetch every assignment available belonging to this project and the current sandbox mode
        assignments_available = {
            assignment.id_assignment: assignment.status_external for assignment in Assignment.objects.filter(
                hit__batch__project=database_object_project,
                hit__batch__use_sandbox=use_sandbox
            )
        }

        # fetch the id of every worker in the database
        dictionary_workers_available = {worker.id_worker: worker for worker in Worker.objects.all()}

        # iterate over every HIT in this project and current sandbox mode where
        #   not all assignments are already in the database or
        #   not all assignments have a final state (approved or rejected)
        for index, hit in enumerate(HIT.objects.annotate(
            count_assignments_current=Coalesce(Count(
                'assignments',
                distinct=True
            ), 0) + F('count_assignments_dead'),
            count_assignments_annotated=Coalesce(Count(
                'assignments',
                distinct=True,
                filter=Q(assignments__status_external__isnull=False)
            ), 0) + F('count_assignments_dead')
        ).annotate(
            all_assignments_are_annotated=Case(
                When(count_assignments_current=F('count_assignments_annotated'),
                     then=True
                ),
                default=False,
                output_field=BooleanField()
            )
        ).filter(
            batch__use_sandbox=use_sandbox,
            batch__project=database_object_project,
        ).exclude(
            # TODO: add additional_assignments to calculation
            count_assignments_current=F('batch__settings_batch__count_assignments'),
            all_assignments_are_annotated=True
        ).select_related('batch')):
            print('##################### hit with index {}'.format(index))
            # print(hit.count_assignments_current)
            # print(hit.all_assignments_are_annotated)
            # print(hit.batch.settings_batch.count_assignments)

            # init the boto3 paginator for the operation 'list_assignments_for_hit'
            paginator = Manager_Projects.get_mturk_api(use_sandbox).get_paginator('list_assignments_for_hit')

            # fetch assignments for the current hit
            response_iterator = paginator.paginate(
                HITId=hit.id_hit,
                AssignmentStatuses=[
                    'Submitted',
                    'Approved',
                    'Rejected'
                ],
                PaginationConfig={
                    'PageSize': 100,
                }
            )

            for iterator in response_iterator:
                for assignment in iterator['Assignments']:
                    id_assignment: str = assignment['AssignmentId'].upper()
                    id_worker: str = assignment['WorkerId'].upper()
                    status_mturk: str = assignment['AssignmentStatus']

                    # if the assignment is not already in the database
                    if not id_assignment in assignments_available:
                        # check whether the worker is already in the database
                        try:
                            worker = dictionary_workers_available[id_worker]
                        except KeyError:
                            # otherwise create the new worker and add it to the dictionary
                            worker = Worker.objects.get_or_create(
                                id_worker=id_worker,
                            )[0]
                            dictionary_workers_available[id_worker] = worker

                        status = None
                        if status_mturk == 'Approved':
                            status = assignments.STATUS_EXTERNAL.APPROVED
                        elif status_mturk == 'Rejected':
                            status = assignments.STATUS_EXTERNAL.REJECTED

                        try:
                            answer: str = json.dumps(xmltodict.parse(assignment['Answer']))
                        except KeyError:
                            answer: str = json.dumps({})

                        # create the assignment in the database
                        assignment = Assignment.objects.create(
                            id_assignment=id_assignment,
                            hit=hit,
                            worker=worker,
                            status_external=status,
                            answer=answer,
                            datetime_submit=assignment['SubmitTime'],
                            datetime_accept=assignment['AcceptTime'],
                        )
                    # if the assignment is already in the database,
                    # check whether the annotatation state corresponds with the database state
                    else:
                        status: assignments.STATUS_EXTERNAL = mturk_status_to_database_status(status_mturk)

                        # if the assignment from mturk has a different state than the assignment of mturk
                        if status != assignments_available[id_assignment]:
                            # update the status of the assignment
                            Assignment.objects.filter(
                                id_assignment=id_assignment
                            ).update(
                                status_external=status
                            )

            # if hit is expired
            if hit.datetime_expiration < timezone.now():
                # add dead assignments
                print('expired')
                hit_new = HIT.objects.filter(
                    pk=hit.pk
                ).annotate(
                    count_assignments_current=Coalesce(Count(
                        'assignments',
                        distinct=True
                    ), 0) + F('count_assignments_dead'),
                ).annotate(
                    assignments_dead=F('batch__settings_batch__count_assignments') - F('count_assignments_current'),
                    count_assignments_dead_new=F('count_assignments_dead') + F('assignments_dead')
                ).get()

                # TODO: add additional_assignments to calculation
                hit_new.count_assignments_dead = hit_new.count_assignments_dead_new
                hit_new.save()

        return {
            'success': True
        }
        # return Batch.objects.filter(id__in=ids_batch_changed)

    @staticmethod
    def clear_sandbox(database_object_project):
        # import time
        # time.sleep(2)
        queryset_batches = Batch.objects.filter(
            use_sandbox=True,
            project=database_object_project,
        )

        queryset_batches.delete()

    @staticmethod
    def download(database_object_project, request):
        response = HttpResponse(content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename=' + 'results.csv'

        list_ids_batch = request.query_params.getlist('batches[]')
        # check if all values should be downloaded
        set_values_filtered = request.query_params.getlist('values[]')
        if len(set_values_filtered) > 0:
            set_values_filtered = set(set_values_filtered)
        else:
            set_values_filtered = None

        set_answer = Manager_Batches.get_set_answer(list_ids_batch)

        queryset = Assignment.objects.filter(
            hit__batch__id__in=list_ids_batch
        ).select_related(
            'hit__batch__settings_batch__template_worker', 'worker'
        ).order_by(
            'hit__batch__settings_batch__template_worker',
            'hit__batch',
            'hit',
        )

        set_header = None
        writer = None
        for index, assignment in enumerate(queryset.iterator()):
            real_values_in_template = json.loads(assignment.hit.batch.settings_batch.template_worker.json_dict_parameters).keys()

            dict_question = json.loads(assignment.hit.parameters)
            dict_question = {key: dict_question.get(key) for key in real_values_in_template}

            dict_answer = json.loads(Manager_Batches.normalize_answer(assignment.answer))

            dict_result = collections.OrderedDict()
            dict_result['id_assignment'] = assignment.id_assignment
            dict_result['id_hit'] = assignment.hit.id_hit
            dict_result['id_worker'] = assignment.worker.id_worker
            dict_result['sandbox'] = assignment.hit.batch.use_sandbox
            dict_result['creation'] = assignment.hit.datetime_creation
            dict_result['expiration'] = assignment.hit.datetime_expiration
            dict_result['status_external'] = 'SUBMITTED' if assignment.status_external is None else STATUS_EXTERNAL(assignment.status_external).name
            dict_result['status_internal'] = 'SUBMITTED' if assignment.status_internal is None else STATUS_INTERNAL(assignment.status_internal).name
            dict_result.update(dict_question)
            dict_result.update(dict_answer)

            # add missing fields due to possibly different answer-dictionaries (caused by checkboxes, radiobuttons, ...)
            for value in set_answer:
                if value not in dict_answer:
                    dict_result[value] = None

            if set_values_filtered is not None:
                for key in dict_result.keys():
                    if key not in set_values_filtered:
                        del dict_result[key]
                # dict_result = {key: value for key, value in dict_result.items() if key in set_values_filtered}

            # print(sorted(dict_result.keys()))

            if index == 0:
                list_header = list(dict_result.keys())
                # set_header = set(list_header)
                # for answer in set_answer:
                #     if answer not in set_header:
                #         list_header.append(answer)

                # update set_header
                set_header = set(list_header)
                writer = csv.DictWriter(response, fieldnames=list_header)
                writer.writeheader()

            # try:
            writer.writerow(dict_result)
            # except ValueError:
                # writer.writerow({key: dict_result.get(key, None) for key in set_header})

        return response

    @staticmethod
    def get_set_answer(list_ids_batch):
        queryset = Assignment.objects.filter(
            hit__batch__id__in=list_ids_batch
        ).values_list('answer', flat=True)

        set_answer = set()
        for index, answer in enumerate(queryset.iterator()):
            dict_answer = json.loads(Manager_Batches.normalize_answer(answer))
            set_answer = set_answer.union(set(dict_answer.keys()))

        return set_answer

    @staticmethod
    def normalize_answer(answer):
        dict_answer = json.loads(answer)
        normalize_answer = {}

        try:
            for value in dict_answer['QuestionFormAnswers']['Answer']:
                normalize_answer[value['QuestionIdentifier']] = value['FreeText']
        except TypeError:
            normalize_answer[dict_answer['QuestionFormAnswers']['Answer']['QuestionIdentifier']] = \
            dict_answer['QuestionFormAnswers']['Answer']['FreeText']

        return json.dumps(normalize_answer)

    @staticmethod
    def download_info(database_object_project, request):
        list_ids_batch = request.query_params.getlist('batches[]')

        queryset = Batch.objects.filter(
            id__in=list_ids_batch
        ).select_related(
            'settings_batch__template_worker'
        )

        is_valid = True
        set_parameters_last = None
        # set_answer_last = None
        for index, batch in enumerate(queryset):
            # print(batch)
            dict_parameters = json.loads(batch.settings_batch.template_worker.json_dict_parameters)
            set_parameters = set(dict_parameters.keys())

            if index > 0:
                set_difference_parameters = set_parameters.symmetric_difference(set_parameters_last)
                if len(set_difference_parameters) > 0:
                    is_valid = False
                    break

            # set_answer = None
            # assignment = Assignment.objects.filter(hit__batch=batch).first()
            # if assignment is not None:
            #     dict_answer = json.loads(Manager_Batches.normalize_answer(assignment.answer))
            #     set_answer = set(dict_answer.keys())
            #     if set_answer_last is not None:
            #         set_difference_answer = set_answer.symmetric_difference(set_answer_last)
            #         if len(set_difference_answer) > 0:
            #             is_valid = False
            #             break

            set_parameters_last = dict_parameters
            # set_answer_last = set_answer
            # print(dict_parameters)

        set_builtin = set()
        set_builtin.add('id_assignment')
        set_builtin.add('id_hit')
        set_builtin.add('id_worker')
        set_builtin.add('sandbox')
        set_builtin.add('creation')
        set_builtin.add('expiration')
        set_builtin.add('status_external')
        set_builtin.add('status_internal')

        result = {
            'is_valid': is_valid,
        }

        if is_valid == True:
            result.update({
                'set_parameters': set_parameters_last,
                'set_answer':  Manager_Batches.get_set_answer(list_ids_batch),
                'set_builtin': set_builtin,
            })

        return result
