from mturk_manager.views import code_shared
from django.shortcuts import render, redirect
from mturk_manager.models import *
from viewer.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Value, Count
from django.db.models.functions import Concat
import urllib.parse
from django.utils.html import escape
import csv
import io
import random
import json
import time
from django.contrib import messages

glob_prefix_name_tag_batch = 'batch_'

def project(request, name):
    queryset = m_Project.objects.select_related(
        'fk_account_mturk'
    ).prefetch_related(
        'templates', 'batches__hits__assignments'
    )


    context = {}
    name_quoted = name
    name = urllib.parse.unquote(name_quoted)
    try:
        db_obj_project = queryset.get(name=name)
    except ObjectDoesNotExist:
        messages.error(request, 'Project "{}" does not exist'.format(name))
        return redirect('mturk_manager:index')
    # create_data_dummy(db_obj_project)
    # client = code_shared.get_client(db_obj_project)
    # print(client.get_account_balance())

    # print(client.get_hit(HITId='3EHIMLB7F7Z7ME11ZQIIHDZXLIA8H2'))

    if request.method == 'POST':
        if request.POST['task'] == 'synchronize_database':
            synchronize_database(db_obj_project, request)
        if request.POST['task'] == 'create_batch':
            create_batch(db_obj_project, request)
        elif request.POST['task'] == 'add_template':
            add_template(db_obj_project, request)
        elif request.POST['task'] == 'delete_templates':
            delete_templates(db_obj_project, request)
        elif request.POST['task'] == 'update_settings':
            update_settings(db_obj_project, request)

        # db_obj_project = queryset.get(name=name)

        return redirect('mturk_manager:project', name=name_quoted, permanent=True)

    stats = queryset.aggregate(
        count_hits=Count('batches__hits'), 
        count_assignments=Count('batches__hits__assignments')
    )

    context['stats'] = stats
    context['db_obj_project'] = db_obj_project
    return render(request, 'mturk_manager/project.html', context)

def synchronize_database(db_obj_project, request):
    client = code_shared.get_client(db_obj_project)
    set_id_assignments_available = set([assignment.id_assignment for assignment in m_Assignment.objects.all()])
    print(set_id_assignments_available)

    dict_workers_available = {worker.name: worker for worker in m_Worker.objects.all()}
    dict_tags = {tag.name: tag for tag in m_Tag.objects.filter(key_corpus=db_obj_project.name)}
    db_obj_tag_submitted = m_Tag.objects.get(key_corpus=db_obj_project.name, name='submitted')

    for db_obj_hit in m_Hit.objects.annotate(
        count_assignments_current=Count('assignments')
    ).filter(
        fk_batch__fk_project=db_obj_project,
        count_assignments_current__lt=F('fk_batch__count_assignments')
    ).select_related('fk_batch'):
        db_obj_tag = dict_tags[glob_prefix_name_tag_batch+db_obj_hit.fk_batch.name]

        response = client.list_assignments_for_hit(
            HITId=db_obj_hit.id_hit,
            AssignmentStatuses=['Submitted']
        )
        for assignment in response['Assignments']:
            id_assignment = assignment['AssignmentId']
            id_worker = assignment['WorkerId']
            if not id_assignment in set_id_assignments_available:
                print(assignment)
                try:
                    db_obj_worker = dict_workers_available[id_worker]
                except KeyError:
                    db_obj_worker = m_Worker.objects.create(name=id_worker)

                db_obj_assignment = m_Assignment.objects.create(
                    id_assignment=id_assignment,
                    fk_hit=db_obj_hit,
                    fk_worker=db_obj_worker
                )

                db_obj_entity = m_Entity.objects.create(
                    key_corpus=db_obj_project.name,
                    id_item=db_obj_assignment.id,
                    id_item_internal=db_obj_assignment.id
                )
                db_obj_tag.m2m_entity.add(db_obj_entity)
                db_obj_tag_submitted.m2m_entity.add(db_obj_entity)

    # for db_obj_batch in db_obj_project.batches.all():
    #     pass
    #     count_assignments = db_obj_batch.count_assignments
    #     for db_obj_hit in db_obj_batch.hits.annotate(count_assignments_current=Count('assignments')).filter(count_assignments_current__lt=count_assignments):
    #         pass
        #     response = client.list_assignments_for_hit(
        #         HITId=db_obj_hit.id_hit,
        #         AssignmentStatuses=['Submitted']
        #     )
        #     for assignment in response['Assignments']:
        #         print(assignment)

def delete_templates(db_obj_project, request):
    m_Template.objects.filter(
        fk_project=db_obj_project, name__in=request.POST.getlist('templates')
    ).update(
        name=Concat(
            F('name'),
            Value('_'+str(int(time.time())))
        ),
        is_active=False
    )

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
    db_obj_project.keywords = request.POST['keywords']
    db_obj_project.reward = request.POST['reward']
    db_obj_project.lifetime = request.POST['lifetime']
    db_obj_project.duration = request.POST['duration']
    db_obj_project.count_assignments = request.POST['count_assignments']

    if request.POST['template_main'] != '':
        db_obj_project.fk_template_main = m_Template.objects.get(fk_project=db_obj_project, name=request.POST['template_main'])

    db_obj_project.save()

def create_batch(db_obj_project, request):
    if not verify_input_create_batch(request):
        return 

    count_assignments = int(request.POST['count_assignments'])
    lifetime = int(request.POST['lifetime'])
    duration = int(request.POST['duration'])
    reward = request.POST['reward']
    title = request.POST['title']
    description = request.POST['description']
    keywords = request.POST['keywords']


    db_obj_batch = code_shared.glob_create_batch(db_obj_project, request)
    client = code_shared.get_client(db_obj_project)
    reader = csv.DictReader(io.StringIO(request.FILES['file_csv'].read().decode('utf-8')))
    db_obj_template = m_Template.objects.get(fk_project=db_obj_project, name=request.POST['template'])
    # list_entities = []
    for dict_parameters in reader:
        mturk_obj_hit = client.create_hit(
            Keywords=keywords,
            MaxAssignments=count_assignments,
            LifetimeInSeconds=lifetime,
            AssignmentDurationInSeconds=duration,
            Reward=reward,
            Title=title,
            Description=description,
            Question=code_shared.create_question(db_obj_template.template, db_obj_template.height_frame, dict_parameters)
        )

        # print(mturk_obj_hit)
        db_obj_hit = m_Hit.objects.create(
            # id_hit=str(random.randint(0, 9999999)),
            id_hit=mturk_obj_hit['HIT']['HITId'],
            fk_batch=db_obj_batch,
            parameters=json.dumps(dict_parameters)
        )

        # list_assignments

        # list_entities.append(db_obj_hit.id)

    db_obj_tag = m_Tag.objects.get_or_create(
        name=glob_prefix_name_tag_batch+db_obj_batch.name,
        key_corpus=db_obj_project.name
    )[0]

    # m_Entity.objects.bulk_create([m_Entity(id_item=id_hit, id_item_internal=id_hit, key_corpus=db_obj_project.name) for id_hit in list_entities])
    
    # db_obj_tag.m2m_entity.add(*m_Entity.objects.filter(key_corpus=db_obj_project.name, id_item_internal__in=list_entities))

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
        if int(request.POST['count_assignments']) == 0:
            valid = False
            list_messages.append('Invalid number of assignments')
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
        if int(request.POST['count_assignments']) == 0:
            valid = False
            list_messages.append('Invalid number of assignments')
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
        # if request.POST['name'].strip() == '':
        #     valid = False
        #     list_messages.append('Invalid name')
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

