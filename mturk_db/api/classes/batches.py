from api.classes.projects import Manager_Projects
from api.models import Batch, Template_Worker, HIT, Settings_Batch
# from viewer.models import m_Tag
# from api.views import code_shared, project
# from api.views.project import glob_prefix_name_tag_batch, glob_prefix_name_tag_worker, glob_prefix_name_tag_hit
import uuid, json, datetime
from botocore.exceptions import ClientError
from django.db.models import F, Value, Count, Q, Sum, IntegerField, ExpressionWrapper

class Manager_Batches(object):
    @classmethod
    def get_all(cls, database_object_project, use_sandbox=True):
        queryset_batch = Batch.objects.filter(project=database_object_project, use_sandbox=use_sandbox)
        return queryset_batch

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
        name_batch = uuid.uuid4().hex

        settings_batch = Settings_Batch.objects.create(
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

        database_object_batch = Batch.objects.create(
            name=name_batch,
            project=database_object_project,
            use_sandbox=use_sandbox,
            settings_batch=settings_batch,
        )
        database_object_batch.save()

        title = dictionary_settings_batch['title']
        if dictionary_settings_batch['has_content_adult'] == True:
            title = 'Contains adult content! {}'.format(title)


        # return database_object_batch
        for index, dictionary_hit in enumerate(data['data_csv']):
            try:
                # mturk_obj_hit = client.create_hit(
                #     Keywords=','.join([keyword['text'] for keyword in dictionary_settings_batch['keywords']]),
                #     MaxAssignments=dictionary_settings_batch['count_assignments'],
                #     LifetimeInSeconds=dictionary_settings_batch['lifetime'],
                #     AssignmentDurationInSeconds=dictionary_settings_batch['duration'],
                #     AutoApprovalDelayInSeconds=1209600,
                #     Reward=dictionary_settings_batch['reward'],
                #     Title=title,
                #     Description=dictionary_settings_batch['description'],
                #     Question=cls.create_question(dictionary_settings_batch['template_worker'].template, dictionary_settings_batch['template_worker'].height_frame, dictionary_hit),
                #     QualificationRequirements=[]
                #     # QualificationRequirements=cls.get_qualifications(data)
                # )
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
            # db_obj_hit = HIT.objects.create(
            #     # id_hit=str(random.randint(0, 9999999)),
            #     id_hit=mturk_obj_hit['HIT']['HITId'],
            #     batch=database_object_batch,
            #     parameters=json.dumps(dictionary_hit),
            #     datetime_expiration=mturk_obj_hit['HIT']['Expiration'],
            #     datetime_creation=mturk_obj_hit['HIT']['CreationTime'],
            # )
            db_obj_hit = HIT.objects.create(
                # id_hit=str(random.randint(0, 9999999)),
                id_hit=uuid.uuid4().hex,
                batch=database_object_batch,
                parameters=json.dumps(dictionary_hit),
                datetime_expiration=datetime.datetime.now(),
                datetime_creation=datetime.datetime.now(),
            )

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

    # @classmethod
    # def preprocess_template_request(cls, db_obj_project, html_template):
    #     host = code_shared.get_url_block_worker(db_obj_project) 
    #     # path = reverse('mturk_manager:api_status_worker', kwargs={'name':db_obj_project.name, 'id_worker':'a'})[:-1]
    #     # url = urllib.parse.urljoin(host, path)
    #     url = host
    #     injected = ''
    #     injected += '''
    #         <script>
    #             var rkreu = '{url}';
    #             {code_block}
    #         </script>
    #     '''.format(
    #         url=url,
    #         code_block=code_shared.get_code_block_request(),
    #     )

    #     html_template = html_template.replace('</head>', '{}</head>'.format(injected))
    #     return html_template

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
    def sync_mturk(database_object_project):
        batches = Batch.objects.filter(project=database_object_project)

        for db_obj_hit in HIT.objects.annotate(
            count_assignments_current=Count('assignments')
        ).filter(
            batch__use_sandbox=use_sandbox,
            batch__fk_project=db_obj_project,
            count_assignments_current__lt=F('batch__count_assignments')
        ).select_related('batch'):
            print('test')


        print(batches)
        print(batches.count())