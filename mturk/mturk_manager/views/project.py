from mturk_manager.views import code_shared
from django.shortcuts import render, redirect
from mturk_manager.models import *
import urllib.parse
import csv

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
    db_obj_project.title = request.POST['title']
    db_obj_project.description = request.POST['description']
    db_obj_project.reward = request.POST['reward']
    db_obj_project.lifetime = request.POST['lifetime']
    db_obj_project.duration = request.POST['duration']

    if request.POST['template_main'] != '':
        db_obj_project.fk_template_main = m_Template.objects.get(name=request.POST['template_main'])

    db_obj_project.save()

def create_batch(db_obj_project, request):
    db_obj_batch = code_shared.glob_create_batch(db_obj_project, request)
    return

    # for 

        client = code_shared.get_client(db_obj_project)
        mturk_obj_hit = client.create_hit(
            LifetimeInSeconds=request.POST['lifetime'],
            AssignmentDurationInSeconds=request.POST['duration'],
            Reward=request.POST['reward'],
            Title=request.POST['title'],
            Description=request.POST['description'],
            Question=code_shared.create_question(db_obj_project.template, db_obj_project.height_frame)
        )
    print(mturk_obj_hit)
    # db_obj_hit = m_Hit.objects.create()


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

