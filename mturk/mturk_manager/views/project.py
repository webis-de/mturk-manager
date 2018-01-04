from mturk_manager.views import code_shared
from django.shortcuts import render, redirect
from mturk_manager.models import *
import urllib.parse
import csv
import io
from django.contrib import messages

def project(request, name):
    context = {}
    name_quoted = name
    name = urllib.parse.unquote(name_quoted)
    db_obj_project = m_Project.objects.select_related('fk_account_mturk').prefetch_related('templates').get(name=name)
    # create_data_dummy(db_obj_project)
    # client = code_shared.get_client(db_obj_project)
    # print(client.get_account_balance())

    # print(client.get_hit(HITId='3EHIMLB7F7Z7ME11ZQIIHDZXLIA8H2'))


    if request.method == 'POST':
        if request.POST['task'] == 'create_batch':
            create_batch(db_obj_project, request)
        elif request.POST['task'] == 'add_template':
            add_template(db_obj_project, request)
        elif request.POST['task'] == 'delete_templates':
            delete_templates(db_obj_project, request)
        elif request.POST['task'] == 'update_settings':
            update_settings(db_obj_project, request)

        db_obj_project = m_Project.objects.select_related('fk_account_mturk').prefetch_related('templates').get(name=name)

        return redirect('mturk_manager:project', name=name_quoted, permanent=True)

    context['db_obj_project'] = db_obj_project
    return render(request, 'mturk_manager/project.html', context)

def delete_templates(db_obj_project, request):
    for name in request.POST.getlist('templates'):
        m_Template.objects.get(name=name).delete()

def add_template(db_obj_project, request):
    if not verify_input_add_template(request):
        return 

    template = None
    if request.POST['html_template'].strip() == '':
        if 'file_template' in request.FILES:
            if request.FILES['file_template'].charset == None:
                template = request.FILES['file_template'].read().decode('utf-8')
            else:
                template = request.FILES['file_template'].read().decode(request.FILES['file_template'].charset)
    else:
        template = request.POST['html_template']

    m_Template.objects.create(
        name=request.POST['name'],
        template=template,
        height_frame=request.POST['height_frame'],
        fk_project=db_obj_project
    )

def update_settings(db_obj_project, request):
    verify_input_update_settings(request)

    db_obj_project.title = request.POST['title']
    db_obj_project.description = request.POST['description']
    db_obj_project.reward = request.POST['reward']
    db_obj_project.lifetime = request.POST['lifetime']
    db_obj_project.duration = request.POST['duration']

    if request.POST['template_main'] != '':
        db_obj_project.fk_template_main = m_Template.objects.get(name=request.POST['template_main'])

    db_obj_project.save()

def create_batch(db_obj_project, request):
    if not verify_input_create_batch(request):
        return 

    lifetime = int(request.POST['lifetime'])
    duration = int(request.POST['duration'])
    reward = request.POST['reward']
    title = request.POST['title']
    description = request.POST['description']


    db_obj_batch = code_shared.glob_create_batch(db_obj_project, request)
    client = code_shared.get_client(db_obj_project)
    reader = csv.DictReader(io.StringIO(request.FILES['file_csv'].read().decode('utf-8')))
    db_obj_template = m_Template.objects.get(name=request.POST['template'])
    for line in reader:
        print(line)

        mturk_obj_hit = client.create_hit(
            LifetimeInSeconds=lifetime,
            AssignmentDurationInSeconds=duration,
            Reward=reward,
            Title=title,
            Description=description,
            Question=code_shared.create_question(db_obj_template.template, db_obj_template.height_frame)
        )
        print(mturk_obj_hit)
        db_obj_hit = m_Hit.objects.create(fk_batch=db_obj_batch, )


def verify_input_add_template(request):
    valid = True
    list_messages = []

    try:
        if int(request.POST['height_frame']) == 0:
            valid = False
            list_messages.append('Invalid frame height')
        if request.POST['name'].strip() == '':
            valid = False
            list_messages.append('Invalid name')
        if request.POST['html_template'].strip() == '' and not 'file_template' in request.FILES:
            valid = False
            list_messages.append('Invalid template')
    except KeyError:
        list_messages.append('Unexpected error, please cry')
        valid = False

    for message in list_messages:
        messages.error(request, message)

    return valid

def verify_input_update_settings(request):
    valid = True
    list_messages = []

    try:
        if int(request.POST['lifetime']) == 0:
            valid = False
            list_messages.append('Invalid lifetime')
        if int(request.POST['duration']) == 0:
            valid = False
            list_messages.append('Invalid duration')
        if request.POST['reward'].strip() == '':
            valid = False
            list_messages.append('Invalid reward')
        if request.POST['title'].strip() == '':
            valid = False
            list_messages.append('Invalid title')
        if request.POST['description'].strip() == '':
            valid = False
            list_messages.append('Invalid description')
        if request.POST['template_main'].strip() == '':
            valid = False
            list_messages.append('Invalid template')
    except KeyError:
        list_messages.append('Unexpected error, please cry')
        valid = False

    for message in list_messages:
        messages.warning(request, message)

    return valid

def verify_input_create_batch(request):
    valid = True
    list_messages = []

    try:
        if int(request.POST['lifetime']) == 0:
            valid = False
            list_messages.append('Invalid lifetime')
        if int(request.POST['duration']) == 0:
            valid = False
            list_messages.append('Invalid duration')
        if request.POST['reward'].strip() == '':
            valid = False
            list_messages.append('Invalid reward')
        if request.POST['title'].strip() == '':
            valid = False
            list_messages.append('Invalid title')
        if request.POST['description'].strip() == '':
            valid = False
            list_messages.append('Invalid description')
        if request.POST['name'].strip() == '':
            valid = False
            list_messages.append('Invalid name')
        if request.POST['template'].strip() == '':
            valid = False
            list_messages.append('Invalid template')
        if not 'file_csv' in request.FILES:
            valid = False
            list_messages.append('Invalid csv file')
    except KeyError:
        list_messages.append('Unexpected error, please cry')
        valid = False

    for message in list_messages:
        messages.error(request, message)

    return valid

def create_data_dummy(db_obj_project):
    db_obj_batch = m_Batch.objects.get_or_create(
        name='batch_test',
        defaults={
        'fk_project': db_obj_project
        }
    )[0]
    db_obj_hit = m_Hit.objects.get_or_create(
        fk_batch=db_obj_batch
    )[0]
    db_obj_worker = m_Worker.objects.get_or_create(
        name='Kristof'
    )[0]
    db_obj_worker1 = m_Worker.objects.get_or_create(
        name='Martin'
    )[0]

    m_Assignment.objects.bulk_create([
        m_Assignment(id_assignment='id_assignment_1', fk_worker=db_obj_worker, fk_hit=db_obj_hit),
        m_Assignment(id_assignment='id_assignment_2', fk_worker=db_obj_worker1, fk_hit=db_obj_hit),
        m_Assignment(id_assignment='id_assignment_3', fk_worker=db_obj_worker, fk_hit=db_obj_hit),
        m_Assignment(id_assignment='id_assignment_4', fk_worker=db_obj_worker, fk_hit=db_obj_hit),
        m_Assignment(id_assignment='id_assignment_5', fk_worker=db_obj_worker, fk_hit=db_obj_hit),
        m_Assignment(id_assignment='id_assignment_6', fk_worker=db_obj_worker, fk_hit=db_obj_hit),
        m_Assignment(id_assignment='id_assignment_7', fk_worker=db_obj_worker, fk_hit=db_obj_hit),
        m_Assignment(id_assignment='id_assignment_8', fk_worker=db_obj_worker1, fk_hit=db_obj_hit),
        m_Assignment(id_assignment='id_assignment_9', fk_worker=db_obj_worker1, fk_hit=db_obj_hit),
        m_Assignment(id_assignment='id_assignment_0', fk_worker=db_obj_worker, fk_hit=db_obj_hit),
    ])

