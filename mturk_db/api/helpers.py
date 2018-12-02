from rest_framework.pagination import PageNumberPagination

from api.models import Project
from mturk_db.settings import REST_FRAMEWORK


class CustomPagination(PageNumberPagination):
    page_size = REST_FRAMEWORK['PAGE_SIZE']
    page_size_query_param = 'page_size'
    # max_page_size = 10000


def add_database_object_project(some_function):
    def wrapper(*args, **kwargs):
        # import time
        # time.sleep(1)
        try:
            slug_project = kwargs['slug_project']
        except KeyError:
            database_object_project = None
        else:
            database_object_project = Project.objects.get_or_create(slug=slug_project)[0]

        kwargs['database_object_project'] = database_object_project

        try:
            request = args[1]
        except IndexError:
            request = args[0]

        try:
            use_sandbox = False if request.query_params['use_sandbox'] == 'false' else True
        except KeyError:
            use_sandbox = True

        kwargs['use_sandbox'] = use_sandbox

        return some_function(*args, **kwargs)

    return wrapper
def migrate_project(name_project):
    import api.models as models 
    import uuid, json, datetime, xmltodict
    from django.utils.text import slugify
    from django.conf import settings
    import datetime
    print('####################')
    print(name_project)
    database_object_project = models.Project.objects.get_or_create(
        name=name_project,
        defaults={
            'slug': slugify(name_project),
            'version': settings.VERSION_PROJECT,
            'fk_account_mturk':  models.Account_Mturk.objects.all()[0]
        }
    )[0]

    dictionary_templates = {}
    with open('data/{}_templates.ldjson'.format(name_project), 'r') as f:
        for line in f:
            object_template = json.loads(line)

            template = models.Template_Worker.objects.create(
                name='template',
                project=database_object_project,
                template=object_template['template'],
                height_frame=object_template['height_frame'],
                json_dict_parameters=object_template['json_dict_parameters'],
            )

            dictionary_templates[object_template['id']] = template


    dictionary_batches = {}
    with open('data/{}_batches.ldjson'.format(name_project), 'r') as f:
        for line in f:
            try:
                object_batch = json.loads(line)
            except:
                raise Exception(line)
            print(object_batch)



            database_object_batch = models.Batch.objects.create(
                name=object_batch['name'],
                project=database_object_project,
                use_sandbox=False,
            )

            settings_batch = models.Settings_Batch.objects.create(
                batch=database_object_batch,
                project=database_object_project,
                name='{}__{}__{}'.format(database_object_project.id, object_batch['name'], uuid.uuid4().hex),

                title=object_batch['settings_batch']['title'],
                reward=object_batch['settings_batch']['reward'],
                count_assignments=object_batch['settings_batch']['count_assignments'],
                # count_assignments_max_per_worker=,
                description=object_batch['settings_batch']['description'],
                lifetime=object_batch['settings_batch']['lifetime'],
                duration=object_batch['settings_batch']['duration'],
                # block_workers=dictionary_settings_batch['block_workers'],
                template_worker=dictionary_templates[object_batch['settings_batch']['template_worker']],

                # has_content_adult=dictionary_settings_batch['has_content_adult'],
                # qualification_assignments_approved=dictionary_settings_batch['qualification_assignments_approved'],
                # qualification_hits_approved=dictionary_settings_batch['qualification_hits_approved'],
                qualification_locale=json.dumps([]),

            )

            # settings_batch.keywords.set([keyword['id'] for keyword in dictionary_settings_batch['keywords']])

            dictionary_batches[object_batch['name']] = database_object_batch

    dictionary_hits = {}
    with open('data/{}_hits.ldjson'.format(name_project), 'r') as f:
        for line in f:
            object_hit = json.loads(line)

            hit = models.HIT.objects.create(
                id_hit=object_hit['id_hit'],
                batch=dictionary_batches[object_hit['name_batch']],
                datetime_creation=datetime.datetime.utcfromtimestamp(object_hit['datetime_creation']),
                datetime_expiration=datetime.datetime.utcfromtimestamp(object_hit['datetime_expiration']),
                count_assignments_additional=object_hit['count_assignments_additional'],
                parameters=object_hit['parameters'],
            )

            dictionary_hits[object_hit['id_hit']] = hit

    dictionary_workers = {}
    with open('data/{}_workers.ldjson'.format(name_project), 'r') as f:
        for line in f:
            object_worker = json.loads(line)

            worker = models.Worker.objects.get_or_create(
                id_worker=object_worker['id_worker'],
                defaults= {
                    'is_blocked_global': object_worker['is_blocked_global'],
                }
            )[0]

            dictionary_workers[object_worker['id_worker']] = worker

    dictionary_assignments = {}
    with open('data/{}_assignments.ldjson'.format(name_project), 'r') as f:
        for line in f:
            object_assignment = json.loads(line)

            status_external = assignments.STATUS_EXTERNAL.APPROVED if 'approved' in object_assignment['tags'] or 'approved_externally' in object_assignment['tags'] else assignments.STATUS_EXTERNAL.REJECTED
            status_internal = assignments.STATUS_INTERNAL.APPROVED if 'approved' in object_assignment['tags'] or 'rejected_externally' in object_assignment['tags'] else assignments.STATUS_INTERNAL.REJECTED

            assignment = models.Assignment.objects.create(
                id_assignment=object_assignment['id_assignment'],
                hit=dictionary_hits[object_assignment['id_hit']],
                answer=object_assignment['answer'],
                worker=dictionary_workers[object_assignment['id_worker']],
                status_external=status_external,
                status_internal=status_internal,
            )

            dictionary_assignments[object_assignment['id_assignment']] = assignment


    dictionary_workers = {worker.id_worker: worker for worker in models.Worker.objects.all()}

    # dictionary_workers = {}
    with open('data/{}_workers_block_project.ldjson'.format(name_project), 'r') as f:
        data_workers = json.loads(f.read())
        list_blocks_soft = data_workers['blocks']['soft']
        dictionary_counters = data_workers['counters']

        for id_worker in list_blocks_soft:
            try:
                worker = dictionary_workers[id_worker]
            except:
                print('passed block: {}'.format(id_worker))
                continue

            models.Worker_Block_Project.objects.create(project=database_object_project, worker=dictionary_workers[id_worker])


        for id_worker, limit in dictionary_counters.items():
            try:
                worker = dictionary_workers[id_worker]
            except:
                print('passed limit: {}'.format(id_worker))
                continue

            models.Count_Assignments_Worker_Project.objects.create(
                project=database_object_project, 
                worker=dictionary_workers[id_worker],
                count_assignments=limit
            )

        # for line in f:
        #     object_worker = json.loads(line)

        #     worker = models.Worker.objects.get_or_create(
        #         id_worker=object_worker['id_worker'],
        #         defaults= {
        #             'is_blocked_global': object_worker['is_blocked_global'],
        #         }
        #     )[0]

        #     dictionary_workers[object_worker['id_worker']] = worker