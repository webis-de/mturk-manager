from mturk_manager.models import *
from viewer.models import *
from mturk_manager.views import code_shared


def migration_2(db_obj_project):
    m_Tag.objects.create(
        key_corpus=db_obj_project.name,
        name='rejected externally',
        color='#dc3545'
    )
    m_Tag.objects.create(
        key_corpus=db_obj_project.name,
        name='approved externally',
        color='#28a745'
    )

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

dict_migrations = {
    1: [
        {
            'type': 'update_config_file',
            'key': 'cards',
            'content': [{'content': ''' 
                <div class="mb-2">
                    <span data-inject="count_selected_rows"></span> Assignment(s) selected
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
    ]
}