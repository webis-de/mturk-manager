from mturk_manager.classes.projects import Manager_Projects
from mturk_manager.models import m_Template, m_Batch, m_Hit
from viewer.models import m_Tag
from mturk_manager.views import code_shared, project
# from mturk_manager.views.project import glob_prefix_name_tag_batch, glob_prefix_name_tag_worker, glob_prefix_name_tag_hit
import uuid, json
from botocore.exceptions import ClientError

class Manager_Batches(object):

    @classmethod
    def create(cls, database_object_project, data, use_sandbox=True):
        client = Manager_Projects.get_mturk_api(database_object_project, use_sandbox)
        print(use_sandbox)
        print(database_object_project)
        print(data)

        dictionary_settings_batch = data['settings']

        print('+++++++++++++++++++++++++++')
        print(dictionary_settings_batch)
        print(dictionary_settings_batch['keywords'])
        print(dictionary_settings_batch['assignments_max'])
        print(dictionary_settings_batch['lifetime'])
        print(dictionary_settings_batch['duration'])
        print(dictionary_settings_batch['reward'])
        print(dictionary_settings_batch['title'])
        print(dictionary_settings_batch['description'])
        print(dictionary_settings_batch['template'])
        print('missing: AutoApprovalDelayInSeconds, Question, QualificationRequirement')
        print('+++++++++++++++++++++++++++')

        database_object_template_worker = m_Template.objects.get(id=dictionary_settings_batch['template'])
        # print(database_object_template_worker)

        if dictionary_settings_batch['block_workers']:
            database_object_template_worker.template = cls.preprocess_template_request(database_object_project, database_object_template_worker.template)

        # print(database_object_template_worker.template)

        database_object_batch = m_Batch.objects.create(
            name=uuid.uuid4().hex,
            fk_project=database_object_project,
            title=dictionary_settings_batch['title'],
            description=dictionary_settings_batch['description'],
            count_assignments=dictionary_settings_batch['assignments_max'],
            use_sandbox=use_sandbox,
            reward=dictionary_settings_batch['reward'],
            lifetime=dictionary_settings_batch['lifetime'],
            duration=dictionary_settings_batch['duration'],
            fk_template=database_object_template_worker,
        )
        print(dictionary_settings_batch['keywords'])
        database_object_batch.keywords.set([keyword['id'] for keyword in dictionary_settings_batch['keywords']])
        database_object_batch.save()

        for dictionary_hit in data['data_csv']:
            try:
                mturk_obj_hit = client.create_hit(
                    Keywords='kritten',
                    MaxAssignments=dictionary_settings_batch['assignments_max'],
                    LifetimeInSeconds=dictionary_settings_batch['lifetime'],
                    AssignmentDurationInSeconds=dictionary_settings_batch['duration'],
                    AutoApprovalDelayInSeconds=1209600,
                    Reward=dictionary_settings_batch['reward'],
                    Title=dictionary_settings_batch['title'],
                    Description=dictionary_settings_batch['description'],
                    Question=code_shared.create_question(database_object_template_worker.template, database_object_template_worker.height_frame, dictionary_hit),
                    QualificationRequirements=[]
                )
            except ClientError as e:
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

            db_obj_tag = m_Tag.objects.create(
                name=project.glob_prefix_name_tag_hit+mturk_obj_hit['HIT']['HITId'],
                key_corpus=database_object_project.name
            )

            # print(mturk_obj_hit)
            db_obj_hit = m_Hit.objects.create(
                # id_hit=str(random.randint(0, 9999999)),
                id_hit=mturk_obj_hit['HIT']['HITId'],
                fk_batch=database_object_batch,
                parameters=json.dumps(dictionary_hit),
                datetime_expiration=mturk_obj_hit['HIT']['Expiration'],
                datetime_creation=mturk_obj_hit['HIT']['CreationTime'],
            )

        db_obj_tag = m_Tag.objects.get_or_create(
            name=project.glob_prefix_name_tag_batch+database_object_batch.name,
            key_corpus=database_object_project.name
        )[0]
    #     for index_reader, dict_parameters in enumerate(reader):
    #     # print(index_reader)
    #     # print(len(dict_parameters))
    #     # print(dict_parameters)
    #     try:
    #         mturk_obj_hit = client.create_hit(
    #             Keywords='',
    #             # Keywords=form.cleaned_data['keywords'],
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

        return {}

    @classmethod
    def preprocess_template_request(cls, db_obj_project, html_template):
        host = code_shared.get_url_block_worker(db_obj_project) 
        # path = reverse('mturk_manager:api_status_worker', kwargs={'name':db_obj_project.name, 'id_worker':'a'})[:-1]
        # url = urllib.parse.urljoin(host, path)
        url = host
        injected = ''
        injected += '''
            <script>
                var rkreu = '{url}';
                {code_block}
            </script>
        '''.format(
            url=url,
            code_block=code_shared.get_code_block_request(),
        )

        html_template = html_template.replace('</head>', '{}</head>'.format(injected))
        return html_template