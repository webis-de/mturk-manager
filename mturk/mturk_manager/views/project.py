from mturk_manager.views import code_shared
from django.shortcuts import render, redirect
from mturk_manager.models import *
import urllib.parse

def project(request, name):
    # create_data_dummy(db_obj_project)
    context = {}
    name = urllib.parse.unquote(name)
    db_obj_project = m_Project.objects.select_related('fk_account_mturk').get(name=name)

    if request.method == 'POST':
        if request.POST['task'] == 'create_batch':
            print('create_batch')
            create_batch(db_obj_project, request.POST)
            pass

    	
    context['db_obj_project'] = db_obj_project
    return render(request, 'mturk_manager/project.html', context)

def create_batch(db_obj_project, dict_post):
    code_shared.glob_create_batch(db_obj_project, dict_post['name'])

def create_data_dummy(db_obj_project):
    db_obj_batch = m_Batch.objects.get_or_create(
        name='batch_test',
        fk_project=db_obj_project
    )[0]
    m_Hit.objects.get_or_create(
        fk_batch=db_obj_batch
    )[0]

