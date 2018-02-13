from django.shortcuts import render, redirect
from mturk_manager.models import *
from viewer.models import *
from viewer.views.shared_code import glob_manager_data
from django.urls import reverse
from django.conf import settings
import urllib.parse
import json

glob_dict_settings = {
    # possible values: 'csv-file', 'ldjson-file', 'custom', 'database'
    'name': '',
    'description': '',
    'data_type': 'database',
    # name of the app where the model is located
    'app_label': 'mturk_manager',
    # name of the model
    'model_name': 'm_Assignment',
    'database_filters': {
        'fk_hit__fk_batch__fk_project__name': 'PLACEHOLDER_NAME'
    },
    'database_select_related': [
        'fk_hit__fk_batch', 
        'fk_worker'
    ],
    'database_prefetch_related': [
        'corpus_viewer_tags'
    ],
    'data_fields': {
        # 'id': {
        #     'type': 'number',
        #     'display_name': 'ID'
        # },
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
    },
    'id': 'id_assignment',
    'displayed_fields': [
        'id_assignment', 
        'fk_hit__id_hit', 
        'fk_worker__name', 
        'fk_hit__fk_batch__use_sandbox',
        'fk_hit__datetime_creation',
        'fk_hit__datetime_expiration',
    ],
    'page_size': 25,
    'filters': [
        {
            'data_field': 'fk_hit__fk_batch__use_sandbox',
            'description': 'Sandbox',
            'placeholder': '',
        },
    ],
    'urls_header': [],
    # 'secret_token_editing': '',
    'cards': [
        {
            'name': 'MTurk',
            'content': ''' 
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
                            let url = 'PLACEHOLDER_URL_VIEW?list_ids=';
                            const list_ids = [];
                            $.each(glob_selected_items, function( i, val ) {
                                list_ids.push(val.viewer__id_item_internal);
                            });
                            url += JSON.stringify(list_ids);
                            window.open(url, '_blank');
                            console.log(glob_selected_items)
                        });

                        $(document).on('click', '#button_mturk_download', function(){
                            let url = 'PLACEHOLDER_URL_DOWNLOAD?list_ids=';

                            const list_ids = [];
                            $.each(glob_selected_items, function( i, val ) {
                                list_ids.push(val.viewer__id_item_internal);
                            });
                            url += JSON.stringify(list_ids);
                            window.open(url, '_blank');
                        });
                    });
                </script>'''
        }
    ],
}

glob_dict_settings_workers = {
    'name': '',
    'description': '',
    'data_type': 'database',
    'app_label': 'mturk_manager',
    'model_name': 'm_Worker',
    'database_filters': {
        'fk_project__name': 'PLACEHOLDER_NAME'
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

def create(request):
    context = {}
    context['queryset_account_mturk'] = m_Account_Mturk.objects.all()

    if request.method == 'POST':
        print(request.COOKIES)
        print(request.POST)
        print(request.FILES)
        if not verify_input(request) == True:
            context['success'] = False
            return render(request, 'mturk_manager/create.html', context)
            
        create_project(request)

        context['success'] = True
        return redirect('mturk_manager:project', name=urllib.parse.quote(request.POST['name'], safe=''))
    

    return render(request, 'mturk_manager/create.html', context)

def create_project(request):
    db_obj_account_mturk = m_Account_Mturk.objects.get(name=request.POST['name_account_mturk'])

    db_obj_project = m_Project.objects.create(
        version=settings.VERSION_PROJECT,
        name=request.POST['name'],
        fk_account_mturk = db_obj_account_mturk,
    )

    add_corpus_assignments(request)
    add_corpus_workers(request)
    glob_manager_data.check_for_new_corpora()
    
    m_Template_Assignment.objects.create(
        name='default_template_assignment__'+db_obj_project.name,
        fk_project=db_obj_project,
        template='<b>Please set a custom assignment template!</b>',
        is_active=False
    )
    
    m_Template_Hit.objects.create(
        name='default_template_hit__'+db_obj_project.name,
        fk_project=db_obj_project,
        template='<div class="col-12"><div data-inject_assignments></div></div>',
        is_active=False
    )

    m_Tag.objects.create(
        key_corpus=request.POST['name'],
        name='submitted',
        color='#17a2b8'
    )
    m_Tag.objects.create(
        key_corpus=request.POST['name'],
        name='rejected',
        color='#dc3545'
    )
    m_Tag.objects.create(
        key_corpus=request.POST['name'],
        name='approved',
        color='#28a745'
    )
    m_Tag.objects.create(
        key_corpus=request.POST['name'],
        name='rejected externally',
        color='#dc3545'
    )
    m_Tag.objects.create(
        key_corpus=request.POST['name'],
        name='approved externally',
        color='#28a745'
    )

def add_corpus_workers(request):
    dict_settings = glob_dict_settings_workers.copy()
    dict_settings['name'] = 'Workers'

    dict_settings['urls_header'] = [
        {
            'link': reverse('mturk_manager:project', args=[request.POST['name']]),
            'name': 'Project'
        },
        {
            'link': reverse('mturk_manager:documentation'),
            'name': 'Documentation'
        },
        {
            'link': reverse('mturk_manager:index'),
            'name': 'Open/Add Project'
        },
        {
            'link': reverse('mturk_manager:settings'),
            'name': 'Settings'
        }
    ]
    
    for key, value in dict_settings['database_filters'].items():
        dict_settings['database_filters'][key] = dict_settings['database_filters'][key].replace('PLACEHOLDER_NAME', request.POST['name'])
    
    glob_manager_data.add_settings_corpus(request.POST['name'] + '_workers', dict_settings)
    
def add_corpus_assignments(request):
    dict_settings = glob_dict_settings.copy()
    dict_settings['name'] = request.POST['name']

    dict_settings['urls_header'] = [
        {
            'link': reverse('mturk_manager:project', args=[request.POST['name']]),
            'name': 'Project'
        },
        {
            'link': reverse('mturk_manager:documentation'),
            'name': 'Documentation'
        },
        {
            'link': reverse('mturk_manager:index'),
            'name': 'Open/Add Project'
        },
        {
            'link': reverse('mturk_manager:settings'),
            'name': 'Settings'
        }
    ]

    for key, value in dict_settings['database_filters'].items():
        dict_settings['database_filters'][key] = dict_settings['database_filters'][key].replace('PLACEHOLDER_NAME', request.POST['name'])

    for card in dict_settings['cards']:
        card['content'] = card['content'].replace(
            'PLACEHOLDER_URL_VIEW', reverse('mturk_manager:view', args=[request.POST['name']])
        ).replace(
            'PLACEHOLDER_URL_DOWNLOAD', reverse('mturk_manager:download', args=[request.POST['name']])
        )

    glob_manager_data.add_settings_corpus(request.POST['name'], dict_settings)

def verify_input(request):
    try:
        if request.POST['name'].strip() == '':
            return False
    except KeyError:
        return False

    return True

import os
import csv
import json

def load_data(item_handle):
    print('function 2')

    # for x in range(0,10):
    #     obj = {}
    #     obj['id'] = x
    #     obj['text'] = 'this is only a test test'

    item_handle.add({'id':0, 'text': 'test'})
    item_handle.add({'id':1, 'text': 'test test abc'})
    item_handle.add({'id':2, 'text': 'Test test '})
    item_handle.add({'id':5, 'text': 'abc test test'})
    item_handle.add({'id':3, 'text': 'TESTTEST'})
    item_handle.add({'id':4, 'text': ''})