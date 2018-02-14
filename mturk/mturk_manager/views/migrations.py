from mturk_manager.models import *
from viewer.models import *
from mturk_manager.views import code_shared
from mturk_manager.views import create
from django.conf import settings as settings_django
import os
import pprint

def migration_6(db_obj_project):
    set_workers_handled = set()

    for db_obj_batch in db_obj_project.batches.all():
        for db_obj_hit in db_obj_batch.hits.all():
            for db_obj_assignment in db_obj_hit.assignments.select_related('fk_worker__fk_project').all():
                if db_obj_assignment.fk_worker_id in set_workers_handled:
                    continue

                if db_obj_assignment.fk_worker.fk_project == None:
                    db_obj_assignment.fk_worker.fk_project = db_obj_project
                    db_obj_assignment.fk_worker.save()
                else:
                    db_obj_worker = m_Worker.objects.create(
                        name=db_obj_assignment.fk_worker.name,
                        fk_project=db_obj_project,
                    )
                    
                set_workers_handled.add(db_obj_assignment.fk_worker_id)

def migration_5(db_obj_project):
    try:
        path_settings_files = settings_django.PATH_FILES_SETTINGS
    except:
        path_settings_files = os.path.join('..', 'settings')

    with open(os.path.join(path_settings_files, '{}_workers.py'.format(db_obj_project.name)), 'w') as f:
        settings_corpus_workers = {
            'name': 'Workers',
            'description': '',
            'data_type': 'database',
            'app_label': 'mturk_manager',
            'model_name': 'm_Worker',
            'database_filters': {
                'fk_project__name': db_obj_project.name
            },
            'database_select_related': [
            ],
            'database_prefetch_related': [
                'assignments'
            ],
            'data_fields': {
                'id': {
                    'type': 'number',
                    'display_name': 'ID'
                },
                'name': {
                    'type': 'string',
                    'display_name': 'Name'
                },
                'is_blocked': {
                    'type': 'boolean',
                    'display_name': 'Blocked'
                },
            },
            'id': 'id',
            'displayed_fields': [
                'name', 
                'is_blocked', 
            ],
            'page_size': 25,
            'filters': [
                {
                    'data_field': 'is_blocked',
                    'description': 'Blocked',
                    'placeholder': '',
                },
            ],
            'urls_header': [],
            'cards': [
            ],
        }
        content = 'DICT_SETTINGS_VIEWER = '+pprint.pformat(settings_corpus_workers)
        f.write(content)

def migration_3(db_obj_project):
    client_sandbox = code_shared.get_client(db_obj_project, True)
    client_real = code_shared.get_client(db_obj_project, False)

    queryset = m_Hit.objects.filter(fk_batch__fk_project=db_obj_project.id)

    for hit in queryset:
        client = client_sandbox if hit.fk_batch.use_sandbox else client_real

        mturk_obj_hit = client.get_hit(HITId=hit.id_hit)['HIT']
        hit.datetime_expiration = mturk_obj_hit['Expiration']
        hit.datetime_creation = mturk_obj_hit['CreationTime']
        hit.save()

def migration_2(db_obj_project):
    m_Tag.objects.create(
        key_corpus=db_obj_project.name,
        name='rejected externally',
        color='#ffff00'
    )
    m_Tag.objects.create(
        key_corpus=db_obj_project.name,
        name='approved externally',
        color='#ffbf00'
    )

dict_migrations = {
    7: [
        {
            'type': 'update_config_file_workers',
            'key': 'cards',
            'content': [{'content': ''' 
                <div class="mb-2">
                    <span data-inject="count_selected_rows">0</span> Worker(s) selected
                </div>
                <div class="mb-2">
                    <button type="button" id="button_mturk_unblock" class="btn btn-sm btn-success">Unblock</button>
                    <button type="button" id="button_mturk_block" class="btn btn-sm btn-danger">Block</button>
                </div>
                <script>
                    $(document).ready(function()
                    {
                        $(document).on('click', '#button_mturk_unblock', function(){
                            let data = {};
                            data.task = 'unblock_workers';

                            const list_ids = [];
                            $.each(glob_selected_items, function( i, val ) {
                                list_ids.push(val.viewer__id_item_internal);
                            });

                            data.list_ids = list_ids
                            console.log(data)
                            $.ajax({
                                url: '/project/${name_project}/api',
                                method: 'POST',
                                dataType: 'json',
                                headers: {'X-CSRFToken':$('input[name="csrfmiddlewaretoken"]').val()},
                                data: data,
                                success: function(result) {
                                    load_current_page();
                                }
                            });
                        });

                        $(document).on('click', '#button_mturk_block', function(){
                            let data = {};
                            data.task = 'block_workers';

                            const list_ids = [];
                            $.each(glob_selected_items, function( i, val ) {
                                list_ids.push(val.viewer__id_item_internal);
                            });

                            data.list_ids = list_ids
                            console.log(data)
                            $.ajax({
                                url: '/project/${name_project}/api',
                                method: 'POST',
                                dataType: 'json',
                                headers: {'X-CSRFToken':$('input[name="csrfmiddlewaretoken"]').val()},
                                data: data,
                                success: function(result) {
                                    load_current_page();
                                }
                            });
                        });
                    });
                </script>''',
            'name': 'MTurk'}]
        }
    ],
    6: [
        {
            'type': 'update_config_file_workers',
            'key': 'database_related_name',
            'content': 'corpus_viewer_workers'
        },
        {
            'type': 'execute_function',
            'function': migration_6
        }
    ],
    1: [
        {
            'type': 'update_config_file',
            'key': 'cards',
            'content': [{'content': ''' 
                <div class="mb-2">
                    <span data-inject="count_selected_rows">0</span> Assignment(s) selected
                </div>
                <div class="mb-2">
                    <button type="button" id="button_mturk_approve" class="btn btn-sm btn-success">Approve</button>
                    <button type="button" id="button_mturk_reject" class="btn btn-sm btn-danger">Reject</button>
                </div>
                <div class="mb-2">
                    <a class="btn btn-sm btn-info" id="button_mturk_view" href="#">View assignments</a>
                </div>
                <div>
                    <button type="button" id="button_mturk_download" class="btn btn-sm btn-primary">Download results</button>
                </div>
                <script>
                    $(document).ready(function()
                    {
                        $(document).on('update.cv.selected-items', function(e, list_items) { console.log(e);console.log(list_items) });

                        $(document).on('click', '#button_mturk_view', function(){
                            let url = '/view/${name_project}?list_ids=';
                            const list_ids = [];
                            $.each(glob_selected_items, function( i, val ) {
                                list_ids.push(val.viewer__id_item_internal);
                            });
                            url += JSON.stringify(list_ids);
                            window.open(url, '_blank');
                            console.log(glob_selected_items)
                        });

                        $(document).on('click', '#button_mturk_download', function(){
                            let url = '/project/${name_project}/download?list_ids=';

                            const list_ids = [];
                            $.each(glob_selected_items, function( i, val ) {
                                list_ids.push(val.viewer__id_item_internal);
                            });
                            url += JSON.stringify(list_ids);
                            window.open(url, '_blank');
                        });
                    });
                </script>''',
            'name': 'MTurk'}]
        }
    ], 
    2: [
        {
            'type': 'execute_function',
            'function': migration_2,
        }
    ],
    3: [
        {
            'type': 'execute_function',
            'function':  migration_3
        }
    ],
    4: [
        {
            'type': 'update_config_file',
            'key': 'data_fields',
            'content': {
                'id_assignment': {
                    'type': 'string',
                    'display_name': 'ID'
                },
                'fk_hit__id_hit': {
                    'type': 'string',
                    'display_name': 'HIT'
                },
                'fk_worker__name': {
                    'type': 'string',
                    'display_name': 'Worker'
                },
                'fk_hit__fk_batch__use_sandbox': {
                    'type': 'boolean',
                    'display_name': 'Sandbox'
                },
                'fk_hit__datetime_creation': {
                    'display_name': 'Creation', 
                    'type': 'string'
                },
                'fk_hit__datetime_expiration': {
                    'display_name': 'Expiration', 
                    'type': 'string'
                }
            }
        },
        {
            'type': 'update_config_file',
            'key': 'displayed_fields',
            'content': [
                'id_assignment', 
                'fk_hit__id_hit', 
                'fk_worker__name', 
                'fk_hit__fk_batch__use_sandbox',
                'fk_hit__datetime_creation',
                'fk_hit__datetime_expiration',
            ]
        }
    ],
    5: [
        {
            'type': 'execute_function',
            'function':  migration_5
        }
    ]
}