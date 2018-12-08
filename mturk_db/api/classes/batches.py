from django.db.models.functions import Coalesce

from api.classes.projects import Manager_Projects
from api.models import Batch, Template_Worker, HIT, Assignment, Settings_Batch, Worker
# from viewer.models import m_Tag
# from api.views import code_shared, project
# from api.views.project import glob_prefix_name_tag_batch, glob_prefix_name_tag_worker, glob_prefix_name_tag_hit
import uuid, json, datetime, xmltodict
from botocore.exceptions import ClientError
from django.db.models import F, Value, Count, Q, Sum, IntegerField, ExpressionWrapper
from django.conf import settings as settings_django

class Manager_Batches(object):
    # @classmethod
    # def get_all(cls, database_object_project, use_sandbox=True):
    #     # import time
    #     # time.sleep(2)
    #     queryset_batch = Batch.objects.filter(project=database_object_project, use_sandbox=use_sandbox)
    #     return queryset_batch

    @classmethod
    def create(cls, database_object_project, data, use_sandbox=True):

        client = Manager_Projects.get_mturk_api(use_sandbox)
        # client = Manager_Projects.get_mturk_api(database_object_project, use_sandbox)
        print(use_sandbox)
        print(database_object_project)
        print(data)
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
            dictionary_settings_batch['template_worker'].template = cls.preprocess_template_request(database_object_project, dictionary_settings_batch['template_worker'].template)

        # print(data['template_worker'].template)
        try:
            name_batch = data['name']
        except KeyError:
            name_batch = uuid.uuid4().hex

        database_object_batch = Batch.objects.create(
            name=name_batch,
            project=database_object_project,
            use_sandbox=use_sandbox,
        )

        settings_batch = Settings_Batch.objects.create(
            batch=database_object_batch,
            project=database_object_project,
            name='{}__{}__{}'.format(database_object_project.id, name_batch, uuid.uuid4().hex),

            title=dictionary_settings_batch['title'],
            reward=dictionary_settings_batch['reward'],
            count_assignments=dictionary_settings_batch['count_assignments'],
            count_assignments_max_per_worker=dictionary_settings_batch['count_assignments_max_per_worker'],
            description=dictionary_settings_batch['description'],
            lifetime=dictionary_settings_batch['lifetime'],
            duration=dictionary_settings_batch['duration'],
            block_workers=dictionary_settings_batch['block_workers'],
            template_worker=dictionary_settings_batch['template_worker'],

            has_content_adult=dictionary_settings_batch['has_content_adult'],
            qualification_assignments_approved=dictionary_settings_batch['qualification_assignments_approved'],
            qualification_hits_approved=dictionary_settings_batch['qualification_hits_approved'],
            qualification_locale=json.dumps(dictionary_settings_batch['qualification_locale']),

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
                    Reward=cls.cent_to_dollar(dictionary_settings_batch['reward']),
                    Title=title,
                    Description=dictionary_settings_batch['description'],
                    Question=cls.create_question(dictionary_settings_batch['template_worker'].template, dictionary_settings_batch['template_worker'].height_frame, dictionary_hit),
                    QualificationRequirements=[]
                    # QualificationRequirements=cls.get_qualifications(data)
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
                id_hit=mturk_obj_hit['HIT']['HITId'],
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
        # batches = Batch.objects.filter(project=database_object_project)

        set_id_assignments_available = set([assignment.id_assignment for assignment in Assignment.objects.filter(hit__batch__project=database_object_project, hit__batch__use_sandbox=use_sandbox)])
        print(set_id_assignments_available)
        dictionary_workers_available = {worker.id_worker: worker for worker in Worker.objects.all()}
        # dictionary_workers_available = {worker.id_worker: worker for worker in Worker.objects.filter(project=database_object_project)}

        ids_batch_changed = set();

        for hit in HIT.objects.annotate(
            count_assignments_current=Count('assignments')
        ).filter(
            batch__use_sandbox=use_sandbox,
            batch__project=database_object_project,
            count_assignments_current__lt=F('batch__settings_batch__count_assignments')
        ).select_related('batch'):
            # print(hit.id_hit)
            # print(hit.count_assignments_current)
            paginator = Manager_Projects.get_mturk_api(use_sandbox).get_paginator('list_assignments_for_hit')

            response_iterator = paginator.paginate(
                HITId=hit.id_hit,
                AssignmentStatuses=[
                    'Submitted',
                ],
                PaginationConfig={
                    'PageSize': 100,
                }
            )

            for iterator in response_iterator:
                for assignment in iterator['Assignments']:
                    id_assignment = assignment['AssignmentId']
                    id_worker = assignment['WorkerId']
                    print(id_assignment)
                    # print(id_worker)
                    # print(iterator)

                    if not id_assignment in set_id_assignments_available:
                        try:
                            worker = dictionary_workers_available[id_worker]
                        except KeyError:
                            worker = Worker.objects.get_or_create(
                                id_worker=id_worker,
                                # project=database_object_project,
                            )[0]
                            dictionary_workers_available[id_worker] = worker

                        ids_batch_changed.add(hit.batch.id)

                        assignment = Assignment.objects.create(
                            id_assignment=id_assignment,
                            hit=hit,
                            worker=worker,
                            answer=json.dumps(xmltodict.parse(assignment['Answer'])),
                        )

        # print(batches)
        # print(batches.count())

        return Batch.objects.filter(id__in=ids_batch_changed)

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
    def get(database_object_project, use_sandbox, request):
        queryset = Batch.objects.filter(
            project=database_object_project,
            use_sandbox=use_sandbox,
        ).annotate(
            count_hits=Count('hits')
        ).annotate(
            count_assignments_available=Coalesce(Count('hits__assignments', distinct=True), 0),
            count_assignments_total=F('count_hits') * F('settings_batch__count_assignments')
        )

        sort_by = request.query_params.get('sort_by')
        if sort_by is not None:
            descending = request.query_params.get('descending', 'false') == 'true'
            queryset = queryset.order_by(
                ('-' if descending else '') + sort_by
            )

        return queryset