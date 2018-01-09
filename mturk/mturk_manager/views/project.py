from mturk_manager.views import code_shared
from django.shortcuts import render, redirect
from mturk_manager.models import *
from viewer.models import *
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Value, Count
from django.db.models.functions import Concat
import urllib.parse
from django.utils.html import escape
from django.db import IntegrityError
from botocore.exceptions import ClientError
import csv
import io
import random
import html
import json
import time
from django.contrib import messages, humanize
import xmltodict
from viewer.views.shared_code import glob_manager_data
# from django.template.defaultfilters import apnumber

glob_prefix_name_tag_batch = 'batch_'
glob_prefix_name_tag_worker = 'worker_'
glob_prefix_name_tag_hit = 'hit_'

def project(request, name):
    context = {}
    name_quoted = name
    name_project = urllib.parse.unquote(name_quoted)

    queryset = m_Project.objects.filter(
        name=name_project
    ).select_related(
        'fk_account_mturk',
        'fk_template_main',
        'fk_template_assignment_main'
    ).prefetch_related(
        'batches__hits__assignments',
        'templates_assignment',
        'templates__fk_template_assignment'
    )


    try:
        db_obj_project = queryset.get()
    except ObjectDoesNotExist:
        messages.error(request, 'Project "{}" does not exist'.format(name_project))
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
        elif request.POST['task'] == 'add_template_assignment':
            add_template_assignment(db_obj_project, request)
        elif request.POST['task'] == 'add_template':
            add_template(db_obj_project, request)
        elif request.POST['task'] == 'update_template':
            update_template(db_obj_project, request)
        elif request.POST['task'] == 'update_template_assignment':
            update_template_assignment(db_obj_project, request)
        elif request.POST['task'] == 'delete_templates':
            delete_templates(db_obj_project, request)
        elif request.POST['task'] == 'delete_templates_assignment':
            delete_templates_assignment(db_obj_project, request)
        elif request.POST['task'] == 'update_settings':
            update_settings(db_obj_project, request)
        elif request.POST['task'] == 'delete_project':
            return delete_project(db_obj_project, request)

        # db_obj_project = queryset.get(name=name)
# ***REMOVED***
# ***REMOVED***
        return redirect('mturk_manager:project', name=name_quoted, permanent=True)

    stats_total = queryset.aggregate(
        count_batches=Count('batches'), 
        count_hits=Count('batches__hits'), 
        count_assignments=Count('batches__hits__assignments')
    )

    stats_new = m_Tag.objects.filter(
        key_corpus=name_project,
        name='submitted'
    ).aggregate(
        count_assignments=Count('m2m_entity')
    )
    count_assignments_new = stats_new['count_assignments']
    if count_assignments_new > 0:
        text = 'There is a new assignment available!' 
        if count_assignments_new > 1:
            text = 'There are {} new assignments available!'.format(count_assignments_new)
        print(reverse('viewer:index', kwargs={'id_corpus':db_obj_project.name}))
        messages.info(request, text+' <a href="{}?viewer__filter_tags=%5B%22submitted%22%5D" class="alert-link">View</a>'.format(
        # messages.warning(request, text+' <a href="{}?viewer__filter_tags[\'submitted\']" class="alert-link">View</a>'.format(
            reverse('viewer:index', kwargs={'id_corpus':db_obj_project.name})
        ))

    context['stats_total'] = stats_total
    context['stats_new'] = stats_new
    context['db_obj_project'] = db_obj_project
    return render(request, 'mturk_manager/project.html', context)

def delete_project(db_obj_project, request):
    glob_manager_data.delete_corpus(db_obj_project.name, False)

    m_Tag.objects.filter(key_corpus=db_obj_project.name).delete()

    db_obj_project.delete()

    messages.success(request, 'Deleted project successfully')

    return redirect('mturk_manager:index', permanent=True)

def synchronize_database(db_obj_project, request):
    client = code_shared.get_client(db_obj_project)
    set_id_assignments_available = set([assignment.id_assignment for assignment in m_Assignment.objects.filter(fk_hit__fk_batch__fk_project=db_obj_project)])
    print(set_id_assignments_available)

    # response = client.list_assignments_for_hit(
    #         HITId='3IZPORCT1F9D4JGXYZOI8UU2BC9RHC',
    #         AssignmentStatuses=['Submitted']
    #     )
    # print(response['Assignments'][0]['Answer'])
    # print(xmltodict.parse(response['Assignments'][0]['Answer']))
    # print(json.dumps(xmltodict.parse(response['Assignments'][0]['Answer']), indent=1))

    dict_workers_available = {worker.name: worker for worker in m_Worker.objects.all()}
    dict_tags = {tag.name: tag for tag in m_Tag.objects.filter(key_corpus=db_obj_project.name)}
    db_obj_tag_submitted = m_Tag.objects.get(key_corpus=db_obj_project.name, name='submitted')

    for db_obj_hit in m_Hit.objects.annotate(
        count_assignments_current=Count('assignments')
    ).filter(
        fk_batch__fk_project=db_obj_project,
        count_assignments_current__lt=F('fk_batch__count_assignments')
    ).select_related('fk_batch'):
        db_obj_tag_batch = dict_tags[glob_prefix_name_tag_batch+db_obj_hit.fk_batch.name]
        db_obj_tag_hit = dict_tags[glob_prefix_name_tag_hit+db_obj_hit.id_hit]

        response = client.list_assignments_for_hit(
            HITId=db_obj_hit.id_hit,
            AssignmentStatuses=['Submitted']
        )
        for assignment in response['Assignments']:
            id_assignment = assignment['AssignmentId']
            id_worker = assignment['WorkerId']
            if not id_assignment in set_id_assignments_available:
                try:
                    db_obj_worker = dict_workers_available[id_worker]
                except KeyError:
                    db_obj_worker = m_Worker.objects.create(name=id_worker)
                    dict_workers_available[id_worker] = db_obj_worker

                db_obj_assignment = m_Assignment.objects.create(
                    id_assignment=id_assignment,
                    fk_hit=db_obj_hit,
                    fk_worker=db_obj_worker,
                    answer=json.dumps(xmltodict.parse(assignment['Answer']))
                )

                db_obj_entity = m_Entity.objects.create(
                    key_corpus=db_obj_project.name,
                    id_item=db_obj_assignment.id,
                    id_item_internal=db_obj_assignment.id
                )
                db_obj_tag_batch.m2m_entity.add(db_obj_entity)
                db_obj_tag_submitted.m2m_entity.add(db_obj_entity)
                db_obj_tag_hit.m2m_entity.add(db_obj_entity)

                db_obj_tag_worker = m_Tag.objects.get_or_create(key_corpus=db_obj_project.name, name=glob_prefix_name_tag_worker+id_worker, defaults={'color': '#0000ff'})[0]
                db_obj_tag_worker.m2m_entity.add(db_obj_entity)

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

def delete_templates_assignment(db_obj_project, request):
    m_Template_Assignment.objects.filter(
        fk_project=db_obj_project, id__in=request.POST.getlist('templates')
    ).update(
        name=Concat(
            F('name'),
            Value('_'+str(int(time.time())))
        ),
        is_active=False
    )

    messages.success(request, 'Deleted template(s) successfully')

def delete_templates(db_obj_project, request):
    m_Template.objects.filter(
        fk_project=db_obj_project, id__in=request.POST.getlist('templates')
    ).update(
        name=Concat(
            F('name'),
            Value('_'+str(int(time.time())))
        ),
        is_active=False
    )

    messages.success(request, 'Deleted template(s) successfully')

def update_template_assignment(db_obj_project, request):
    if not verify_input_update_template_assignment(request):
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

    try:
        if template == None:
            m_Template_Assignment.objects.filter(id=request.POST['id']).update(
                name=request.POST['name'],
            )
        else:
            m_Template_Assignment.objects.filter(id=request.POST['id']).update(
                name=request.POST['name'],
                template=template
            )
    except IntegrityError:
        messages.error(request, 'A template with this name already exists')
        return

    messages.success(request, 'Updated template successfully')

def add_template_assignment(db_obj_project, request):
    if not verify_input_add_template_assignment(request):
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

    try:
        m_Template_Assignment.objects.create(
            name=request.POST['name'],
            template=template,
            fk_project=db_obj_project
        )
    except IntegrityError:
        messages.error(request, 'A template with this name already exists')
        return

    messages.success(request, 'Added template successfully')

def update_template(db_obj_project, request):
    if not verify_input_update_template(request):
        return 

    print(request.POST)

    try:
        if 'template_assignment' in request.POST and request.POST['template_assignment'].strip() != '':
            m_Template.objects.filter(id=request.POST['id']).update(
                name=request.POST['name'],
                height_frame=request.POST['height_frame'],
                fk_template_assignment=m_Template_Assignment.objects.get(id=request.POST['template_assignment'])
            )
        else:
            m_Template.objects.filter(id=request.POST['id']).update(
                name=request.POST['name'],
                height_frame=request.POST['height_frame']
            )

    except IntegrityError:
        messages.error(request, 'A template with this name already exists')
        return

    messages.success(request, 'Updated template successfully')

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

    try:
        db_obj_template_assignment = m_Template_Assignment.objects.get(fk_project=db_obj_project, id=request.POST['template_assignment'])
    except ValueError:
        db_obj_template_assignment = m_Template_Assignment.objects.get(fk_project=db_obj_project, name="default_template_assignment__"+db_obj_project.name)

    try:
        m_Template.objects.create(
            name=request.POST['name'],
            template=template,
            height_frame=request.POST['height_frame'],
            fk_project=db_obj_project,
            fk_template_assignment=db_obj_template_assignment
        )
    except IntegrityError:
        messages.error(request, 'A template with this name already exists')
        return

    messages.success(request, 'Added template successfully')

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
        db_obj_project.fk_template_main = m_Template.objects.get(fk_project=db_obj_project, id=request.POST['template_main'])

    if request.POST['template_assignment_main'] != '':
        db_obj_project.fk_template_assignment_main = m_Template_Assignment.objects.get(fk_project=db_obj_project, id=request.POST['template_assignment_main'])

    db_obj_project.save()

    messages.success(request, 'Updated settings successfully')

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
    db_obj_template = m_Template.objects.get(fk_project=db_obj_project, id=request.POST['template'])
    # list_entities = []
    for dict_parameters in reader:
        try:
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
        except ClientError:
            messages.error(request, 'The HTML template is invalid')
            db_obj_batch.delete()
            return

        db_obj_tag = m_Tag.objects.create(
            name=glob_prefix_name_tag_hit+mturk_obj_hit['HIT']['HITId'],
            key_corpus=db_obj_project.name
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

    messages.success(request, 'Created batch successfully')

    # m_Entity.objects.bulk_create([m_Entity(id_item=id_hit, id_item_internal=id_hit, key_corpus=db_obj_project.name) for id_hit in list_entities])
    
    # db_obj_tag.m2m_entity.add(*m_Entity.objects.filter(key_corpus=db_obj_project.name, id_item_internal__in=list_entities))

def verify_input_add_template_assignment(request):
    valid = True
    list_messages = []

    try:
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

def verify_input_update_template_assignment(request):
    valid = True
    list_messages = []

    try:
        if request.POST['name'].strip() == '':
            valid = False
            list_messages.append('Invalid name')
    except KeyError:
        list_messages.append('Unexpected error, please cry')
        valid = False

    for message in list_messages:
        messages.error(request, message)

    return valid

def verify_input_update_template(request):
    valid = True
    list_messages = []

    print(request.POST)
    try:
        if int(request.POST['height_frame']) == 0:
            valid = False
            list_messages.append('Invalid frame height')
        if request.POST['name'].strip() == '':
            valid = False
            list_messages.append('Invalid name')
    except KeyError:
        list_messages.append('Unexpected error, please cry')
        valid = False

    for message in list_messages:
        messages.error(request, message)

    return valid

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

