import json
import traceback

from botocore.exceptions import ClientError
from celery import shared_task

from api.models import HIT


@shared_task(bind=True, name='tasks.create_batch')
def create_batch(self, data, database_object_project=None, use_sandbox=True):
    from api.classes import Manager_Projects, ManagerTasks, Manager_Batches, Manager_Templates_Worker, Manager_Settings_Batch
    try:
        ManagerTasks.start(self.request.id)

        client = Manager_Projects.get_mturk_api(use_sandbox)
        dictionary_settings_batch = data['settings_batch']

        # inject blocking code into the template
        if dictionary_settings_batch['block_workers']:
            dictionary_settings_batch['template_worker'].template = Manager_Batches.preprocess_template_request(database_object_project, dictionary_settings_batch['template_worker'].template)

        # create batch
        database_object_batch = Manager_Batches.create_batch(
            name_batch=data['name'],
            database_object_project=database_object_project,
            use_sandbox=use_sandbox,
        )

        Manager_Templates_Worker.clone_and_fix_template(dictionary_settings_batch['template_worker'])

        Manager_Settings_Batch.clone_and_fix_settings_batch(
            database_object_project=database_object_project,
            database_object_batch=database_object_batch,
            dictionary_settings_batch=dictionary_settings_batch,
        )


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
                print(traceback.format_exc())
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

            self.update_state(
                state='PROGRESS',
                meta={'current': index + 1, 'total': len(data['data_csv'])}
            )

        ManagerTasks.delete_by_uid(self.request.id)

    except Exception as e:
        ManagerTasks.failed(self.request.id)
        print(traceback.format_exc())
