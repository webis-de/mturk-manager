from django.shortcuts import render, redirect
from mturk_manager.models import *
from viewer.models import *
from mturk_manager.views.migrations import dict_migrations
import urllib.parse
import os
from viewer.views.shared_code import glob_manager_data
import pprint
from django.contrib import messages
from django.conf import settings as settings_django

def settings(request):
    context = {}

    if request.method == 'POST':
        if request.POST['task'] == 'add_account':
            add_account(request)
        if request.POST['task'] == 'update_account':
            update_account(request)
        if request.POST['task'] == 'update_projects':
            update_projects(request)
        return redirect('mturk_manager:settings')

    context['queryset_mturk'] = m_Account_Mturk.objects.all()
    context['queryset_projects'] = m_Project.objects.all().select_related('fk_account_mturk')
    context['version'] = settings_django.VERSION_PROJECT

    return render(request, 'mturk_manager/settings.html', context)

def update_projects(request):
    # for project in m_Project.objects.filter(name='test'):
    try:
        for project in m_Project.objects.filter(version__lt=settings_django.VERSION_PROJECT):
            update_project(project)
    except Exception as e:
        print(e)
        messages.error(request, 'The upgrade process failed!')
    else:
        messages.success(request, 'All projects were updated to the most recent version.')


    glob_manager_data.check_for_new_corpora()

def update_project(db_obj_project):
    for version in range(db_obj_project.version + 1, settings_django.VERSION_PROJECT + 1):
        apply_migration(db_obj_project, dict_migrations[version])

    db_obj_project.version = settings_django.VERSION_PROJECT
    db_obj_project.save()

def apply_migration(db_obj_project, migration):
    try:
        path_settings_files = settings_django.PATH_FILES_SETTINGS
    except:
        path_settings_files = os.path.join('..', 'settings')

    for step in migration:
        if step['type'] == 'update_config_file':
            key = step['key']
            content = step['content']
            settings_corpus_new = None
            with open(os.path.join(path_settings_files, '{}.py'.format(db_obj_project.name)), 'r') as f:
                global_env = {}
                local_env = {}
                compiled = compile(f.read(), '<string>', 'exec')
                exec(compiled, global_env, local_env)
                settings_corpus = local_env['DICT_SETTINGS_VIEWER']
                settings_corpus[key] = content
                settings_corpus_new = settings_corpus

            with open(os.path.join(path_settings_files, '{}.py'.format(db_obj_project.name)), 'w') as f:
                content = 'DICT_SETTINGS_VIEWER = '+pprint.pformat(settings_corpus_new)
                content = content.replace('${name_project}', db_obj_project.name)
                f.write(content)
        elif step['type'] == 'execute_function':
            step['function'](db_obj_project)

def update_account(request):
    if not verify_input_add_account(request):
        return 

    m_Account_Mturk.objects.filter(
        id=request.POST['id']
    ).update(
        name = request.POST['name'],
        key_access = request.POST['key_access'],
        key_secret = request.POST['key_secret'],
    )   

    messages.success(request, 'Updated account successfully')

def add_account(request):
    if not verify_input_add_account(request):
        return 

    m_Account_Mturk.objects.get_or_create(
        name = request.POST['name'],
        key_access = request.POST['key_access'],
        key_secret = request.POST['key_secret'],
    )

    messages.success(request, 'Created account successfully')

def verify_input_add_account(request):
    valid = True
    list_messages = []

    try:
        if request.POST['name'].strip() == '':
            valid = False
            list_messages.append('Invalid name')
        if request.POST['key_access'].strip() == '':
            valid = False
            list_messages.append('Invalid access key')
        if request.POST['key_secret'].strip() == '':
            valid = False
            list_messages.append('Invalid secret key')
    except KeyError:
        list_messages.append('Unexpected error, please cry')
        valid = False

    for message in list_messages:
        messages.error(request, message)

    return valid