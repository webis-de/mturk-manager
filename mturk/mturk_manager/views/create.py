from django.shortcuts import render, redirect
from mturk_manager.models import *
from django.urls import reverse
import urllib.parse
import requests
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
    'data_fields': {
        # 'id': {
        #     'type': 'number',
        #     'display_name': 'ID'
        # },
        'id_assignment': {
            'type': 'string',
            'display_name': 'ID'
        },
        'fk_hit__id': {
            'type': 'string',
            'display_name': 'HIT'
        },
        'fk_worker__name': {
            'type': 'string',
            'display_name': 'Worker'
        }
    },
    'id': 'id_assignment',
    'displayed_fields': [
        'id_assignment', 'fk_hit__id', 'fk_worker__name'
    ],
    'page_size': 10,
    'filters': [],
    'urls_header': []
}

def create(request):
    context = {}
    context['queryset_account_mturk'] = m_Account_Mturk.objects.all()

    if request.method == 'POST':
        print(request.COOKIES)
        print(request.POST)
        print(request.FILES)
        verified_input = verify_input(request)
        if not verified_input == True:
            context['success'] = False
            return render(request, 'mturk_manager/create.html', context)
            
        create_project(request)

        context['success'] = True
        return redirect('mturk_manager:project', name=urllib.parse.quote(request.POST['name'], safe=''), permanent=True)
    

    return render(request, 'mturk_manager/create.html', context)

def create_project(request):
    template = None
    if request.POST['html_template'].strip() == '':
        if request.FILES['file_template'].charset == None:
            template = request.FILES['file_template'].read().decode('utf-8')
        else:
            template = request.FILES['file_template'].read().decode(request.FILES['file_template'].charset)

    else:
        template = request.POST['html_template']

    db_obj_account_mturk = m_Account_Mturk.objects.get(name=request.POST['name_account_mturk'])

    m_Project.objects.get_or_create(
        name=request.POST['name'],
        template = template,
        fk_account_mturk = db_obj_account_mturk,
    )

    dict_settings = glob_dict_settings.copy()
    dict_settings['name'] = request.POST['name']

    dict_settings['urls_header'] = [
        {
            'link': reverse('mturk_manager:project', args=[request.POST['name']]),
            'name': 'Project'
        }
    ]

    print(dict_settings)

    dict_payload = {}
    dict_payload['settings'] = json.dumps(dict_settings)
    dict_payload['id_corpus'] = request.POST['name']
    dict_payload['csrfmiddlewaretoken'] = request.POST['csrfmiddlewaretoken']

    url = request.META['HTTP_ORIGIN'] + reverse('viewer:api_add_corpus')
    response = requests.post(url, data=dict_payload, cookies=request.COOKIES)
    print(response)
    
    url = request.META['HTTP_ORIGIN'] + reverse('viewer:api_refresh_corpora')
    response = requests.get(url)
    print(response)

def verify_input(request):
    try:
        if request.POST['name'].strip() == '':
            return False

        if request.POST['html_template'].strip() == '':
            if 'file_template' not in request.FILES:
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