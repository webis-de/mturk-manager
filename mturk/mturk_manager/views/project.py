from mturk_manager.views import code_shared
from django.shortcuts import render, redirect
from mturk_manager.models import *
from viewer.models import *
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Value, Count, Q
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
        'templates_hit',
        'templates__fk_template_assignment',
        'messages_reject'
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
            synchronize_database(db_obj_project, request, True)
            synchronize_database(db_obj_project, request, False)
        if request.POST['task'] == 'create_batch':
            create_batch(db_obj_project, request)
        elif request.POST['task'] == 'add_template':
            add_template(db_obj_project, request)
        elif request.POST['task'] == 'add_template_assignment':
            add_template_assignment(db_obj_project, request)
        elif request.POST['task'] == 'add_template_hit':
            add_template_hit(db_obj_project, request)
        elif request.POST['task'] == 'add_message_reject':
            add_message_reject(db_obj_project, request)
        elif request.POST['task'] == 'update_template':
            update_template(db_obj_project, request)
        elif request.POST['task'] == 'update_template_assignment':
            update_template_assignment(db_obj_project, request)
        elif request.POST['task'] == 'update_template_hit':
            update_template_hit(db_obj_project, request)
        elif request.POST['task'] == 'update_message_reject':
            update_message_reject(db_obj_project, request)
        elif request.POST['task'] == 'delete_templates':
            delete_templates(db_obj_project, request)
        elif request.POST['task'] == 'delete_templates_hit':
            delete_templates_hit(db_obj_project, request)
        elif request.POST['task'] == 'delete_templates_assignment':
            delete_templates_assignment(db_obj_project, request)
        elif request.POST['task'] == 'delete_messages_reject':
            delete_messages_reject(db_obj_project, request)
        elif request.POST['task'] == 'update_settings':
            update_settings(db_obj_project, request)
        elif request.POST['task'] == 'delete_project':
            return delete_project(db_obj_project, request)

        # db_obj_project = queryset.get(name=name)
        # ***REMOVED***
        # ***REMOVED***
        return redirect('mturk_manager:project', name=name_quoted, permanent=True)

    stats_total = queryset.aggregate(
        count_batches=Count('batches', filter=Q(batches__use_sandbox=False), distinct=True), 
        count_hits=Count('batches__hits', filter=Q(batches__use_sandbox=False), distinct=True), 
        count_assignments=Count('batches__hits__assignments', filter=Q(batches__use_sandbox=False), distinct=True),

        count_batches_sandbox=Count('batches', filter=Q(batches__use_sandbox=True), distinct=True), 
        count_hits_sandbox=Count('batches__hits', filter=Q(batches__use_sandbox=True), distinct=True), 
        count_assignments_sandbox=Count('batches__hits__assignments', filter=Q(batches__use_sandbox=True), distinct=True)
    )

    stats_new = m_Tag.objects.filter(
        key_corpus=name_project,
        name='submitted'
    ).aggregate(
        count_assignments=Count('items', filter=Q(items__fk_hit__fk_batch__use_sandbox=False), distinct=True),
        count_assignments_sandbox=Count('items', filter=Q(items__fk_hit__fk_batch__use_sandbox=True), distinct=True)
    )
    print(stats_new)

    count_assignments_new = stats_new['count_assignments']
    count_assignments_sandbox_new = stats_new['count_assignments_sandbox']
    count_assignments_new_total = count_assignments_new + count_assignments_sandbox_new
    if count_assignments_new_total > 0:
        text = 'There is a new assignment available!' 
        if count_assignments_new_total > 1:
            text = 'There are {} new assignments available!'.format(count_assignments_new_total)
        print(reverse('viewer:index', kwargs={'id_corpus':db_obj_project.name}))
        messages.info(request, text+' <a href="{}?viewer__filter_tags=%5B%22submitted%22%5D" class="alert-link">View</a>'.format(
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

def synchronize_database(db_obj_project, request, use_sandbox):
    client = code_shared.get_client(db_obj_project, use_sandbox)
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
        fk_batch__use_sandbox=use_sandbox,
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
                print(id_assignment)
                try:
                    db_obj_worker = dict_workers_available[id_worker]
                except KeyError:
                    db_obj_worker = m_Worker.objects.create(name=id_worker)
                    dict_workers_available[id_worker] = db_obj_worker

                db_obj_assignment = m_Assignment.objects.create(
                    id_assignment=id_assignment,
                    fk_hit=db_obj_hit,
                    fk_worker=db_obj_worker,
                    answer=json.dumps(xmltodict.parse(assignment['Answer'])),
                )

                db_obj_tag_batch.items.add(db_obj_assignment)
                db_obj_tag_submitted.items.add(db_obj_assignment)
                db_obj_tag_hit.items.add(db_obj_assignment)

                db_obj_tag_worker = m_Tag.objects.get_or_create(key_corpus=db_obj_project.name, name=glob_prefix_name_tag_worker+id_worker, defaults={'color': '#0000ff'})[0]
                db_obj_tag_worker.items.add(db_obj_assignment)

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

def delete_templates_hit(db_obj_project, request):
    m_Template_Hit.objects.filter(
        fk_project=db_obj_project, id__in=request.POST.getlist('templates')
    ).update(
        name=Concat(
            F('name'),
            Value('_'+str(int(time.time())))
        ),
        is_active=False
    )

    messages.success(request, 'Deleted template(s) successfully')

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

def delete_messages_reject(db_obj_project, request):
    m_Message_Reject.objects.filter(
        fk_project=db_obj_project, id__in=request.POST.getlist('messages')
    ).delete()

    messages.success(request, 'Deleted reject message(s) successfully')

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

def update_message_reject(db_obj_project, request):
    if not code_shared.validate_form(request, [
        {'type':'string', 'keys':['message'], 'message': 'Invalid message'},
    ]):
        return 

    m_Message_Reject.objects.filter(id=request.POST['id']).update(
        message=request.POST['message'],
    )

    messages.success(request, 'Updated reject message successfully')

def update_template_hit(db_obj_project, request):
    if not code_shared.validate_form(request, [
        {'type':'string', 'keys':['name'], 'message': 'Invalid name'},
    ]):
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
            m_Template_Hit.objects.filter(id=request.POST['id']).update(
                name=request.POST['name'],
            )
        else:
            m_Template_Hit.objects.filter(id=request.POST['id']).update(
                name=request.POST['name'],
                template=template
            )
    except IntegrityError:
        messages.error(request, 'A template with this name already exists')
        return

    messages.success(request, 'Updated template successfully')

def update_template_assignment(db_obj_project, request):
    if not code_shared.validate_form(request, [
        {'type':'string', 'keys':['name'], 'message': 'Invalid name'},
    ]):
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

def add_template_hit(db_obj_project, request):
    if not code_shared.validate_form(request, [
        {'type':'string', 'keys':['name'], 'message': 'Invalid name'},
        {'type':'template', 'keys':['html_template', 'file_template'], 'message': 'Invalid template'},
    ]):
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
        m_Template_Hit.objects.create(
            name=request.POST['name'],
            template=template,
            fk_project=db_obj_project
        )
    except IntegrityError:
        messages.error(request, 'A template with this name already exists')
        return

    messages.success(request, 'Added template successfully')

def add_template_assignment(db_obj_project, request):
    if not code_shared.validate_form(request, [
        {'type':'string', 'keys':['name'], 'message': 'Invalid name'},
        {'type':'template', 'keys':['html_template', 'file_template'], 'message': 'Invalid template'},
    ]):
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

def add_message_reject(db_obj_project, request):
    if not code_shared.validate_form(request, [
        {'type':'string', 'keys':['message'], 'message': 'Invalid message'},
    ]):
        return 

    m_Message_Reject.objects.create(fk_project=db_obj_project, message=request.POST['message'])

    messages.success(request, 'Added reject message successfully')

def update_template(db_obj_project, request):
    if not code_shared.validate_form(request, [
        {'type':'string', 'keys':['name'], 'message': 'Invalid name'},
        {'type':'number', 'keys':['height_frame'], 'message': 'Invalid frame height'},
    ]):
        return 

    print(request.POST)
    db_obj_template = m_Template.objects.get(id=request.POST['id'])

    if 'template_assignment' in request.POST and request.POST['template_assignment'].strip() != '':
        template_assignment = m_Template_Assignment.objects.get(id=request.POST['template_assignment'])
    else:
        template_assignment = db_obj_template.fk_template_assignment

    if 'template_hit' in request.POST and request.POST['template_hit'].strip() != '':
        template_hit = m_Template_Hit.objects.get(id=request.POST['template_hit'])
    else:
        template_hit = db_obj_template.fk_template_hit

    db_obj_template.name = request.POST['name']
    db_obj_template.height_frame = request.POST['height_frame']
    db_obj_template.fk_template_assignment = template_assignment
    db_obj_template.fk_template_hit = template_hit

    try:
        db_obj_template.save()
    except IntegrityError:
        messages.error(request, 'A template with this name already exists')
        return

    messages.success(request, 'Updated template successfully')

def add_template(db_obj_project, request):
    if not code_shared.validate_form(request, [
        {'type':'string', 'keys':['name'], 'message': 'Invalid name'},
        {'type':'number', 'keys':['height_frame'], 'message': 'Invalid frame height'},
        {'type':'template', 'keys':['html_template', 'file_template'], 'message': 'Invalid template'},
    ]):
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
        db_obj_template_hit = m_Template_Hit.objects.get(fk_project=db_obj_project, id=request.POST['template_hit'])
    except ValueError:
        db_obj_template_hit = m_Template_Hit.objects.get(fk_project=db_obj_project, name="default_template_hit__"+db_obj_project.name)

    try:
        m_Template.objects.create(
            name=request.POST['name'],
            template=template,
            height_frame=request.POST['height_frame'],
            fk_project=db_obj_project,
            fk_template_assignment=db_obj_template_assignment,
            fk_template_hit=db_obj_template_hit
        )
    except IntegrityError:
        messages.error(request, 'A template with this name already exists')
        return

    messages.success(request, 'Added template successfully')

def update_settings(db_obj_project, request):
    code_shared.validate_form(request, [
        {'type':'string', 'keys':['title'], 'message': 'Invalid title', 'state': 'warning'},
        {'type':'string', 'keys':['description'], 'message': 'Invalid description', 'state': 'warning'},
        {'type':'string', 'keys':['reward'], 'message': 'Invalid reward', 'state': 'warning'},
        {'type':'number', 'keys':['count_assignments'], 'message': 'Invalid number of assignments', 'state': 'warning'},
        {'type':'number', 'keys':['lifetime'], 'message': 'Invalid hit lifetime', 'state': 'warning'},
        {'type':'number', 'keys':['duration'], 'message': 'Invalid hit duration', 'state': 'warning'},
        {'type':'string', 'keys':['use_sandbox'], 'message': 'Invalid sandbox mode', 'state': 'warning'},
        {'type':'string', 'keys':['template_main'], 'message': 'Invalid main template', 'state': 'warning'},
    ])



    db_obj_project.title = request.POST['title']
    db_obj_project.description = request.POST['description']
    db_obj_project.keywords = request.POST['keywords']
    db_obj_project.reward = request.POST['reward']
    db_obj_project.lifetime = request.POST['lifetime']
    db_obj_project.duration = request.POST['duration']
    db_obj_project.count_assignments = request.POST['count_assignments']
    db_obj_project.use_sandbox = True if request.POST['use_sandbox'] == '1' else False

    if request.POST['template_main'] != '':
        db_obj_project.fk_template_main = m_Template.objects.get(fk_project=db_obj_project, id=request.POST['template_main'])

    if request.POST['template_assignment_main'] != '':
        db_obj_project.fk_template_assignment_main = m_Template_Assignment.objects.get(fk_project=db_obj_project, id=request.POST['template_assignment_main'])

    db_obj_project.save()

    messages.success(request, 'Updated settings successfully')

def create_batch(db_obj_project, request):
    if not code_shared.validate_form(request, [
        {'type':'number', 'keys':['count_assignments'], 'message': 'Invalid number of assignments'},
        {'type':'number', 'keys':['lifetime'], 'message': 'Invalid lifetime'},
        {'type':'number', 'keys':['duration'], 'message': 'Invalid duration'},
        {'type':'string', 'keys':['reward'], 'message': 'Invalid reward'},
        {'type':'string', 'keys':['title'], 'message': 'Invalid title'},
        {'type':'string', 'keys':['description'], 'message': 'Invalid description'},
        {'type':'string', 'keys':['template'], 'message': 'Invalid worker template'},
    ]):
        return 

    if not 'file_csv' in request.FILES:
        valid = False
        messages.error(request, 'Invalid csv file')
        return  

    db_obj_batch = code_shared.glob_create_batch(db_obj_project, request)
    client = code_shared.get_client(db_obj_project, True if request.POST['use_sandbox'] == '1' else False)
    reader = csv.DictReader(io.StringIO(request.FILES['file_csv'].read().decode('utf-8')))
    db_obj_template = m_Template.objects.get(fk_project=db_obj_project, id=request.POST['template'])
    # list_entities = []
    for dict_parameters in reader:
        try:
            mturk_obj_hit = client.create_hit(
                Keywords=request.POST['keywords'],
                MaxAssignments=int(request.POST['count_assignments']),
                LifetimeInSeconds=int(request.POST['lifetime']),
                AssignmentDurationInSeconds=int(request.POST['duration']),
                Reward=request.POST['reward'],
                Title=request.POST['title'],
                Description=request.POST['description'],
                Question=code_shared.create_question(db_obj_template.template, db_obj_template.height_frame, dict_parameters)
            )
        except ClientError as e:
            messages.error(request, '''
                An error occured
                <a href="#alert_1" data-toggle="collapse" class="alert-link">details</a>
                <p class="collapse mb-0" id="alert_1">
                    {}
                </p>
            '''.format(e))
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