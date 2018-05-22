from mturk_manager.views import code_shared
from django.shortcuts import render, redirect
from mturk_manager.models import *
from viewer.models import *
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Value, Count, Q, Sum, IntegerField, ExpressionWrapper
from django.db.models.functions import Concat
import urllib.parse
from django.utils.html import escape
from django.db import IntegrityError
from botocore.exceptions import ClientError
from mturk_manager.forms import *
import csv
import io
import random
import html
import datetime, pytz
import json
from django.conf import settings as settings_django
import time
from django.contrib import messages, humanize
import xmltodict
import hashlib
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

    # print(m_Worker.objects.get(name='A357BORERBTE76').is_blocked)

    try:
        db_obj_project = queryset.get()
    except ObjectDoesNotExist:
        messages.error(request, 'Project "{}" does not exist'.format(name_project))
        return redirect('mturk_manager:index')

    if not code_shared.is_project_up_to_date(request, db_obj_project, name_project):    
        return redirect('mturk_manager:index')

    #approve assignment#####################################
    for id_assignment in [
        # '340UGXU9DY1CPW1SXK7MLFDBQSPVUV',
    ]:
        set_to_approve(id_assignment, name_project)
        # set_to_internal_reject(id_assignment, name_project)
    ######################################


    # create_data_dummy(db_obj_project)
    # client = code_shared.get_client(db_obj_project, use_sandbox=False)
    # # print(client.get_account_balance())
    # # print(m_Hit.objects.get(id_hit='38G0E1M85M5A2C3Y7I2KXVHNW0WUV7').fk_batch.name)
    # # print(client.get_hit(HITId='3T2HW4QDUV7GJB9VIQCOB76KV3Y9CB'))

    # obj_db_worker = m_Worker.objects.get(name='A3QRYD01WEPHCS')
    # for assignment in obj_db_worker.assignments.all():
    #     response = client.approve_assignment(
    #         AssignmentId=assignment.id_assignment,
    #         OverrideRejection=True
    #     )
    #     print(response)

    if request.method == 'POST':
        if request.POST['task'] == 'synchronize_database':
            synchronize_database(db_obj_project, request, True)
            synchronize_database(db_obj_project, request, False)

        if request.POST['task'] == 'create_batch':
            form = Form_Create_Batch(request.POST, request.FILES, instance=db_obj_project)
            if form.is_valid():
                create_batch(db_obj_project, form, request)
        elif request.POST['task'] == 'add_template':
            add_template(db_obj_project, request)
        elif request.POST['task'] == 'add_template_assignment':
            add_template_assignment(db_obj_project, request)
        elif request.POST['task'] == 'add_template_hit':
            add_template_hit(db_obj_project, request)
        elif request.POST['task'] == 'add_template_global':
            add_template_global(db_obj_project, request)
        elif request.POST['task'] == 'add_message_reject':
            add_message_reject(db_obj_project, request)
        elif request.POST['task'] == 'update_template':
            update_template(db_obj_project, request)
        elif request.POST['task'] == 'add_message_block':
            add_message_block(db_obj_project, request)
        elif request.POST['task'] == 'reactivate_templates':
            reactivate_templates(db_obj_project, request)
        elif request.POST['task'] == 'reactivate_templates_assignment':
            reactivate_templates_assignment(db_obj_project, request)
        elif request.POST['task'] == 'reactivate_templates_hit':
            reactivate_templates_hit(db_obj_project, request)
        elif request.POST['task'] == 'update_template_assignment':
            update_template_assignment(db_obj_project, request)
        elif request.POST['task'] == 'update_template_hit':
            update_template_hit(db_obj_project, request)
        elif request.POST['task'] == 'update_template_global':
            update_template_global(db_obj_project, request)
        elif request.POST['task'] == 'update_message_reject':
            update_message_reject(db_obj_project, request)
        elif request.POST['task'] == 'update_message_block':
            update_message_block(db_obj_project, request)
        elif request.POST['task'] == 'delete_templates':
            delete_templates(db_obj_project, request)
        elif request.POST['task'] == 'delete_templates_hit':
            delete_templates_hit(db_obj_project, request)
        elif request.POST['task'] == 'delete_templates_global':
            delete_templates_global(db_obj_project, request)
        elif request.POST['task'] == 'delete_templates_assignment':
            delete_templates_assignment(db_obj_project, request)
        elif request.POST['task'] == 'delete_messages_reject':
            delete_messages_reject(db_obj_project, request)
        elif request.POST['task'] == 'update_settings':
            form = Form_Update_Project(request.POST, instance=db_obj_project)
            if form.is_valid():
                form.save()
        elif request.POST['task'] == 'delete_project':
            return delete_project(db_obj_project, request)
        elif request.POST['task'] == 'clear_sandbox':
            clear_sandbox(db_obj_project, request)
        elif request.POST['task'] == 'import_csv':
            import_csv(db_obj_project, request)

        # db_obj_project = queryset.get(name=name)
        # ***REMOVED***
        # ***REMOVED***
        return redirect('mturk_manager:project', name=name_quoted)

    else:
        form_update_project = Form_Update_Project(instance=db_obj_project)
        form_create_batch = Form_Create_Batch(instance=db_obj_project)

    dict_stats = get_stats(db_obj_project, queryset)

    count_assignments_new = dict_stats['count_assignments_new']
    count_assignments_sandbox_new = dict_stats['count_assignments_sandbox_new']
    count_assignments_new_total = count_assignments_new + count_assignments_sandbox_new
    if count_assignments_new_total > 0:
        queryset = m_Assignment.objects.filter(
            fk_hit__fk_batch__fk_project=db_obj_project,
            corpus_viewer_tags__name='submitted'
        )

        text = 'There is a new assignment available!' 
        if count_assignments_new_total > 1:
            text = 'There are {} new assignments available!'.format(count_assignments_new_total)
        # print(reverse('viewer:index', kwargs={'id_corpus':db_obj_project.name}))
        messages.info(request, '''
            {} 
            <a href="{}?viewer__filter_tags=%5B%22submitted%22%5D" class="alert-link">View</a> 
            or 
            <a href="{}?list_ids=[{}]" class="alert-link">Annotate</a>'''.format(
                text,
                reverse('viewer:index', kwargs={'id_corpus':db_obj_project.name}),
                reverse('mturk_manager:view', kwargs={'name':db_obj_project.name}),
                ','.join([str(assignment.id) for assignment in queryset])
            )
        )

    list_templates_active = []
    list_templates_inactive = []
    for template in db_obj_project.templates.all():
        if template.is_active:
            list_templates_active.append(template)
        else:
            list_templates_inactive.append(template)
            
    list_templates_assignment_active = []
    list_templates_assignment_inactive = []
    name_default_template = 'default_template_assignment__{}'.format(db_obj_project.name)
    for template in db_obj_project.templates_assignment.all():
        if template.name == name_default_template:
            continue
            
        if template.is_active:
            list_templates_assignment_active.append(template)
        else:
            list_templates_assignment_inactive.append(template)
            
    list_templates_hit_active = []
    list_templates_hit_inactive = []
    name_default_template = 'default_template_hit__{}'.format(db_obj_project.name)
    for template in db_obj_project.templates_hit.all():
        if template.name == name_default_template:
            continue
            
        if template.is_active:
            list_templates_hit_active.append(template)
        else:
            list_templates_hit_inactive.append(template)

    context['list_templates_active'] = list_templates_active
    context['list_templates_inactive'] = list_templates_inactive
    context['list_templates_assignment_active'] = list_templates_assignment_active
    context['list_templates_assignment_inactive'] = list_templates_assignment_inactive
    context['list_templates_hit_active'] = list_templates_hit_active
    context['list_templates_hit_inactive'] = list_templates_hit_inactive

    context['dict_stats'] = dict_stats
    context['db_obj_project'] = db_obj_project
    context['info_texts'] = code_shared.get_info_texts()
    context['form_update_project'] = form_update_project
    context['form_create_batch'] = form_create_batch
    return render(request, 'mturk_manager/project.html', context)

def set_to_internal_reject(id_assignment, name_project):
    obj_db_tag_approve_externally = m_Tag.objects.get(name='approved externally', key_corpus=name_project)
    obj_db_tag_rejected = m_Tag.objects.get(name='rejected', key_corpus=name_project)
    obj_db_assignment = m_Assignment.objects.get(id_assignment=id_assignment)
    for tag in obj_db_assignment.corpus_viewer_tags.all():
        print(tag.name)
        if tag.name == 'approved' or tag.name == 'approved externally' or tag.name == 'rejected externally':
            obj_db_assignment.corpus_viewer_tags.remove(tag)

    obj_db_assignment.corpus_viewer_tags.add(obj_db_tag_approve_externally)
    obj_db_assignment.corpus_viewer_tags.add(obj_db_tag_rejected)

def set_to_approve(id_assignment, name_project):
    obj_db_tag_approve = m_Tag.objects.get(name='approved', key_corpus=name_project)
    obj_db_assignment = m_Assignment.objects.get(id_assignment=id_assignment)
    for tag in obj_db_assignment.corpus_viewer_tags.all():
        print(tag.name)
        if tag.name == 'rejected' or tag.name == 'approved externally' or tag.name == 'rejected externally':
            obj_db_assignment.corpus_viewer_tags.remove(tag)

    obj_db_assignment.corpus_viewer_tags.add(obj_db_tag_approve)

def import_csv(db_obj_project, request):
    if 'file_csv' in request.FILES:
        if request.FILES['file_csv'].charset == None:
            string_csv = request.FILES['file_csv'].read().decode('utf-8')
        else:
            string_csv = request.FILES['file_csv'].read().decode(request.FILES['file_csv'].charset)
        reader = csv.DictReader(string_csv.splitlines())

        db_obj_tag_submitted = m_Tag.objects.get(key_corpus=db_obj_project.name, name='submitted')
        db_obj_tag_rejected = m_Tag.objects.get(key_corpus=db_obj_project.name, name='rejected')
        db_obj_tag_approved = m_Tag.objects.get(key_corpus=db_obj_project.name, name='approved')

        db_obj_tag_batch = None
        for index, row in enumerate(reader):
            if index == 0:
                db_obj_batch = code_shared.glob_create_batch(db_obj_project, dictionary={
                    'name': '',
                    'title': row['Title'],
                    'description': row['Description'],
                    'keywords': row['Keywords'],
                    'count_assignments': row['MaxAssignments'],
                    'use_sandbox': True,
                    'reward': row['Reward'],
                    'lifetime': row['AutoApprovalDelayInSeconds'],
                    'duration': row['AssignmentDurationInSeconds'],                 
                })

                db_obj_tag_batch = m_Tag.objects.get_or_create(
                    name=glob_prefix_name_tag_batch+db_obj_batch.name,
                    key_corpus=db_obj_project.name
                )[0]

                # for key, value in sorted(row.items()):
                #     print('{}: {}'.format(key, value)) 

            dict_parameters = {}
            for key, value in row.items():
                if key.startswith('Input.'):
                    dict_parameters[key[6:]] = value

            db_obj_hit = m_Hit.objects.get_or_create(
                id_hit=row['HITId'],
                fk_batch=db_obj_batch,
                parameters=json.dumps(dict_parameters),
                datetime_expiration=pytz.timezone('US/Pacific').localize(datetime.datetime.strptime(row['Expiration'], "%a %b %d %H:%M:%S PST %Y")),
                datetime_creation=pytz.timezone('US/Pacific').localize(datetime.datetime.strptime(row['CreationTime'], "%a %b %d %H:%M:%S PST %Y")),
            )[0]

            db_obj_tag_hit = m_Tag.objects.get_or_create(
                name=glob_prefix_name_tag_hit+db_obj_hit.id_hit,
                key_corpus=db_obj_project.name
            )[0]


            db_obj_worker = m_Worker.objects.get_or_create(
                name=row['WorkerId'],
                fk_project=db_obj_project,
            )[0]

            dict_parameters = {}
            for key, value in row.items():
                if key.startswith('Answer.'):
                    dict_parameters[key[7:]] = value

            db_obj_assignment = m_Assignment.objects.create(
                id_assignment=row['AssignmentId'],
                fk_hit=db_obj_hit,
                fk_worker=db_obj_worker,
                answer=json.dumps(dict_parameters),
            )

            db_obj_tag_batch.corpus_viewer_items.add(db_obj_assignment)

            if row['AssignmentStatus'] == 'Approved':
                db_obj_tag_approved.corpus_viewer_items.add(db_obj_assignment)
            elif row['AssignmentStatus'] == 'Rejected':
                db_obj_tag_rejected.corpus_viewer_items.add(db_obj_assignment)
            else:
                db_obj_tag_submitted.corpus_viewer_items.add(db_obj_assignment)

            db_obj_tag_hit.corpus_viewer_items.add(db_obj_assignment)

            db_obj_tag_worker = m_Tag.objects.get_or_create(
                key_corpus=db_obj_project.name, 
                name=glob_prefix_name_tag_worker+db_obj_worker.name, defaults={'color': '#0000ff'}
            )[0]

            db_obj_tag_worker.corpus_viewer_items.add(db_obj_assignment)

            # break
            # print(row['first_name'], row['last_name'])

def get_stats(db_obj_project, queryset):
    dict_stats = {}
    dict_stats = queryset.aggregate(
        count_batches=Count('batches', filter=Q(batches__use_sandbox=False), distinct=True), 
        count_hits=Count('batches__hits', filter=Q(batches__use_sandbox=False), distinct=True), 
        count_assignments=Count('batches__hits__assignments', filter=Q(batches__use_sandbox=False), distinct=True),
        # count_assignments_total=Sum(
        #     F('batches__count_assignments'), 
        #     output_field=IntegerField(),
        #     filter=Q(batches__use_sandbox=False)
        # ),

        count_batches_sandbox=Count('batches', filter=Q(batches__use_sandbox=True), distinct=True), 
        count_hits_sandbox=Count('batches__hits', filter=Q(batches__use_sandbox=True), distinct=True), 
        count_assignments_sandbox=Count('batches__hits__assignments', filter=Q(batches__use_sandbox=True), distinct=True),
        # count_assignments_sandbox_total=Sum(
        #     F('batches__count_assignments'), 
        #     output_field=IntegerField(),
        #     filter=Q(batches__use_sandbox=True)
        # )
    )

    dict_stats.update(
        m_Batch.objects.filter(
                fk_project=db_obj_project
            ).annotate(count_hits=Count('hits')
            ).aggregate(
                count_assignments_total=Sum(
                    F('count_assignments') * F('count_hits'), 
                    output_field=IntegerField(),
                    filter=Q(use_sandbox=False)
                ),
                count_assignments_sandbox_total=Sum(
                    F('count_assignments') * F('count_hits'), 
                    output_field=IntegerField(),
                    filter=Q(use_sandbox=True)
                )
            )
    )

    if dict_stats['count_assignments_total'] == None:
        dict_stats['count_assignments_total'] = 0
    if dict_stats['count_assignments_sandbox_total'] == None:
        dict_stats['count_assignments_sandbox_total'] = 0

    dict_stats['count_assignments_pending'] = dict_stats['count_assignments_total'] - dict_stats['count_assignments']
    dict_stats['count_assignments_sandbox_pending'] = dict_stats['count_assignments_sandbox_total'] - dict_stats['count_assignments_sandbox']

    dict_stats.update(
        m_Tag.objects.filter(
            key_corpus=db_obj_project.name,
            name='submitted'
        ).aggregate(
            count_assignments_new=Count('corpus_viewer_items', filter=Q(corpus_viewer_items__fk_hit__fk_batch__use_sandbox=False), distinct=True),
            count_assignments_sandbox_new=Count('corpus_viewer_items', filter=Q(corpus_viewer_items__fk_hit__fk_batch__use_sandbox=True), distinct=True)
        )
    )

    return dict_stats

def clear_sandbox(db_obj_project, request):
    queryset_batches = m_Batch.objects.filter(
        use_sandbox=True,
        fk_project=db_obj_project,
    )

    queryset_batches.delete()

    # queryset_workers = m_Worker.objects.filter(
    #     fk_project=db_obj_project,
    # ).annotate(
    #     count_assignments=Count('assignments')
    # ).filter(
    #     count_assignments=0
    # )
    # queryset_workers.delete()

    # for worker in queryset_workers:
    #     print(worker.count_assignments)
    # print(queryset_workers)

    # queryset_tags = m_Tag.objects.filter(
    #     key_corpus=db_obj_project.name,
    # ).exclude(
    #     name__in=['approved', 'approved externally', 'rejected', 'rejected externally', 'submitted']
    # ).annotate(
    #     count_assignments=Count('corpus_viewer_workers'),
    #     count_items=Count('corpus_viewer_items'),
    # ).filter(
    #     count_assignments=0,
    #     count_items=0,
    # )
    # for worker in queryset_tags:
    #     print(worker.count_assignments)
    #     print(worker.count_items)

    # queryset_tags.filter(
    #     name__startswith='hit_'
    # ).delete()

    # queryset_tags.filter(
    #     name__startswith='worker_'
    # ).delete()

    # queryset_tags.filter(
    #     count_assignments__gt=0,
    #     count_items=0,
    # ).delete()
    # queryset_tags.delete()
    # db_obj_project.objects.filter()

def delete_project(db_obj_project, request):
    glob_manager_data.delete_corpus(db_obj_project.name, False)

    m_Tag.objects.filter(key_corpus=db_obj_project.name).delete()

    db_obj_project.delete()

    messages.success(request, 'Deleted project successfully')

    return redirect('mturk_manager:index')

def create_dummy_assignments(db_obj_project):
    m_Assignment.objects.all().delete()
    m_Hit.objects.all().delete()
    m_Worker.objects.all().delete()

    use_sandbox = True
    dict_workers_available = {worker.name: worker for worker in m_Worker.objects.all()}
    dict_tags = {tag.name: tag for tag in m_Tag.objects.filter(key_corpus=db_obj_project.name)}
    db_obj_tag_submitted = m_Tag.objects.get(key_corpus=db_obj_project.name, name='submitted')

    m_Hit.objects.all().delete()
    db_obj_batch = m_Batch.objects.all().first()
    db_obj_hit = m_Hit.objects.create(
        id_hit='esfesfe',
        fk_batch=db_obj_batch,
        parameters='{}',
    )

    db_obj_tag_batch = m_Tag.objects.get_or_create(key_corpus=db_obj_project.name, name='tag_batch')[0]
    db_obj_tag_hit = m_Tag.objects.get_or_create(key_corpus=db_obj_project.name, name='tag_hit')[0]

    if use_sandbox:
        for x in range(5):
            id_assignment = random.randint(0, 99999)
            id_worker = 'test worker'

            try:
                db_obj_worker = dict_workers_available[id_worker]
            except KeyError:
                db_obj_worker = m_Worker.objects.create(name=id_worker)
                dict_workers_available[id_worker] = db_obj_worker

            db_obj_assignment = m_Assignment.objects.create(
                id_assignment=id_assignment,
                fk_hit=db_obj_hit,
                fk_worker=db_obj_worker,
                answer=json.dumps({
                    'QuestionFormAnswers' : {
                        'Answer': {
                            'QuestionIdentifier': 'answer',
                            'FreeText': id_assignment,
                        }
                    }
                })
            )

            db_obj_tag_batch.corpus_viewer_items.add(db_obj_assignment)
            db_obj_tag_submitted.corpus_viewer_items.add(db_obj_assignment)
            db_obj_tag_hit.corpus_viewer_items.add(db_obj_assignment)

            db_obj_tag_worker = m_Tag.objects.get_or_create(key_corpus=db_obj_project.name, name=glob_prefix_name_tag_worker+id_worker, defaults={'color': '#0000ff'})[0]
            db_obj_tag_worker.corpus_viewer_items.add(db_obj_assignment)


def synchronize_database(db_obj_project, request, use_sandbox):
    # create_dummy_assignments(db_obj_project)
    # return
    client = code_shared.get_client(db_obj_project, use_sandbox)
    set_id_assignments_available = set([assignment.id_assignment for assignment in m_Assignment.objects.filter(fk_hit__fk_batch__fk_project=db_obj_project, fk_hit__fk_batch__use_sandbox=use_sandbox)])
    print(set_id_assignments_available)

    # response = client.list_assignments_for_hit(
    #         HITId='3XWUWJ18TLQAPXEY2SSF19F4ITNUUI',
    #         AssignmentStatuses=['Submitted']
    #     )
    # print(response['Assignments'][0]['Answer'])
    # print(xmltodict.parse(response['Assignments'][0]['Answer']))
    # print(json.dumps(xmltodict.parse(response['Assignments'][0]['Answer']), indent=1))

    dict_workers_available = {worker.name: worker for worker in m_Worker.objects.filter(fk_project=db_obj_project)}
    dict_tags = {tag.name: tag for tag in m_Tag.objects.filter(key_corpus=db_obj_project.name)}
    db_obj_tag_submitted = m_Tag.objects.get(key_corpus=db_obj_project.name, name='submitted')

    # for db_obj_hit in m_Hit.objects.filter(
    #     # fk_batch__use_sandbox=use_sandbox,
    #     # fk_batch__fk_project=db_obj_project,

    #     id_hit__in=[
    #         '38G0E1M85M5A2C3Y7I2KXVHNW0WUV7',
    #         '3XWUWJ18TLQAPXEY2SSF19F4ITNUUI'
    #     ]
    # ).select_related('fk_batch'):
    for db_obj_hit in m_Hit.objects.annotate(
        count_assignments_current=Count('assignments')
    ).filter(
        fk_batch__use_sandbox=use_sandbox,
        fk_batch__fk_project=db_obj_project,
        count_assignments_current__lt=F('fk_batch__count_assignments')
    ).select_related('fk_batch'):

        db_obj_tag_batch = dict_tags[glob_prefix_name_tag_batch+db_obj_hit.fk_batch.name]
        db_obj_tag_hit = dict_tags[glob_prefix_name_tag_hit+db_obj_hit.id_hit]
        paginator = client.get_paginator('list_assignments_for_hit')

        response_iterator = paginator.paginate(
            HITId=db_obj_hit.id_hit,
            AssignmentStatuses=[
                'Submitted',
            ],
            PaginationConfig={
                # 'MaxItems': None,
                'PageSize': 100,
                # 'StartingToken': 'string'
            }
        )
        # response = client.list_assignments_for_hit(
        #     HITId=db_obj_hit.id_hit,
        #     AssignmentStatuses=['Submitted']
        # )
        # print(response['Assignments'])
        count = 0
        for iterator in response_iterator:
            # count += len(iterator['Assignments'])
            for assignment in iterator['Assignments']:
                id_assignment = assignment['AssignmentId']
                id_worker = assignment['WorkerId']
                if not id_assignment in set_id_assignments_available:
                    try:
                        db_obj_worker = dict_workers_available[id_worker]
                    except KeyError:
                        db_obj_worker = m_Worker.objects.create(
                            name=id_worker,
                            fk_project=db_obj_project,
                        )
                        dict_workers_available[id_worker] = db_obj_worker

                    db_obj_assignment = m_Assignment.objects.create(
                        id_assignment=id_assignment,
                        fk_hit=db_obj_hit,
                        fk_worker=db_obj_worker,
                        answer=json.dumps(xmltodict.parse(assignment['Answer'])),
                    )

                    db_obj_tag_batch.corpus_viewer_items.add(db_obj_assignment)
                    db_obj_tag_submitted.corpus_viewer_items.add(db_obj_assignment)
                    db_obj_tag_hit.corpus_viewer_items.add(db_obj_assignment)

                    db_obj_tag_worker = m_Tag.objects.get_or_create(key_corpus=db_obj_project.name, name=glob_prefix_name_tag_worker+id_worker, defaults={'color': '#0000ff'})[0]
                    db_obj_tag_worker.corpus_viewer_items.add(db_obj_assignment)



        print(count)











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

def delete_templates_global(db_obj_project, request):
    list_templates = request.POST.getlist('templates')
    
    queryset = m_Template_Global.objects.filter(
        fk_project=db_obj_project, id__in=list_templates
    ).delete()

    messages.success(request, 'Deleted template(s) successfully')

def delete_templates_hit(db_obj_project, request):
    list_templates = request.POST.getlist('templates')
    
    queryset = m_Template_Hit.objects.filter(
        fk_project=db_obj_project, id__in=list_templates
    ).annotate(
        count_templates=Count('templates_used')
    )

    count_updated_rows = queryset.filter(
        count_templates=0
    ).delete()[0]

    if not count_updated_rows == len(list_templates):
        queryset.filter(
            count_templates__gt=0
        ).update(
            is_active=False
        )

    messages.success(request, 'Deleted template(s) successfully')

def delete_templates_assignment(db_obj_project, request):
    list_templates = request.POST.getlist('templates')
    
    queryset = m_Template_Assignment.objects.filter(
        fk_project=db_obj_project, id__in=list_templates
    ).annotate(
        count_templates=Count('templates_used')
    )

    count_updated_rows = queryset.filter(
        count_templates=0
    ).delete()[0]

    if not count_updated_rows == len(list_templates):
        queryset.filter(
            count_templates__gt=0
        ).update(
            is_active=False
        )

    messages.success(request, 'Deleted template(s) successfully')

def delete_messages_reject(db_obj_project, request):
    m_Message_Reject.objects.filter(
        fk_project=db_obj_project, id__in=request.POST.getlist('messages')
    ).delete()

    messages.success(request, 'Deleted reject message(s) successfully')
    
def delete_templates(db_obj_project, request):
    list_templates = request.POST.getlist('templates')
    
    queryset = m_Template.objects.filter(
        fk_project=db_obj_project, id__in=list_templates
    ).annotate(
        count_batches=Count('batches')
    )

    count_updated_rows = queryset.filter(
        count_batches=0
    ).delete()[0]

    if not count_updated_rows == len(list_templates):
        queryset.filter(
            count_batches__gt=0
        ).update(
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

def update_message_block(db_obj_project, request):
    if not code_shared.validate_form(request, [
        {'type':'string', 'keys':['message'], 'message': 'Invalid message'},
    ]):
        return 

    m_Message_Block.objects.filter(id=request.POST['id']).update(
        message=request.POST['message'],
    )

    messages.success(request, 'Updated block message successfully')

def update_template_global(db_obj_project, request):
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
            m_Template_Global.objects.filter(id=request.POST['id']).update(
                name=request.POST['name'],
            )
        else:
            m_Template_Global.objects.filter(id=request.POST['id']).update(
                name=request.POST['name'],
                template=template
            )
    except IntegrityError:
        messages.error(request, 'A template with this name already exists')
        return

    messages.success(request, 'Updated template successfully')

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

def add_template_global(db_obj_project, request):
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
        m_Template_Global.objects.create(
            name=request.POST['name'],
            template=template,
            fk_project=db_obj_project
        )
    except IntegrityError:
        messages.error(request, 'A template with this name already exists')
        return

    messages.success(request, 'Added template successfully')

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

def add_message_block(db_obj_project, request):
    if not code_shared.validate_form(request, [
        {'type':'string', 'keys':['message'], 'message': 'Invalid message'},
    ]):
        return 

    m_Message_Block.objects.create(fk_project=db_obj_project, message=request.POST['message'])

    messages.success(request, 'Added block message successfully')

def reactivate_templates_assignment(db_obj_project, request):
    list_templates = request.POST.getlist('templates')

    count_updated_rows = m_Template_Assignment.objects.filter(
        fk_project=db_obj_project, id__in=list_templates
    ).update(
        is_active=True
    )

    messages.success(request, 'Activated template(s) successfully')

def reactivate_templates_hit(db_obj_project, request):
    list_templates = request.POST.getlist('templates')

    count_updated_rows = m_Template_Hit.objects.filter(
        fk_project=db_obj_project, id__in=list_templates
    ).update(
        is_active=True
    )

    messages.success(request, 'Activated template(s) successfully')

def reactivate_templates(db_obj_project, request):
    list_templates = request.POST.getlist('templates')

    count_updated_rows = m_Template.objects.filter(
        fk_project=db_obj_project, id__in=list_templates
    ).update(
        is_active=True
    )

    messages.success(request, 'Activated template(s) successfully')

def update_template(db_obj_project, request):
    if not code_shared.validate_form(request, [
        {'type':'string', 'keys':['name'], 'message': 'Invalid name'},
        {'type':'number', 'keys':['height_frame'], 'message': 'Invalid frame height'},
    ]):
        return 

    db_obj_template = m_Template.objects.get(id=request.POST['id'])

    template = None
    if request.POST['html_template'].strip() == '':
        if 'file_template' in request.FILES:
            if request.FILES['file_template'].charset == None:
                template = request.FILES['file_template'].read().decode('utf-8')
            else:
                template = request.FILES['file_template'].read().decode(request.FILES['file_template'].charset)
    else:
        template = request.POST['html_template']

    if not template == None:
        dict_parameters =code_shared.count_parameters_in_template(template)
        db_obj_template.json_dict_parameters = json.dumps(dict_parameters)
        db_obj_template.template = template

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

    dict_parameters = code_shared.count_parameters_in_template(template)

    try:
        m_Template.objects.create(
            name=request.POST['name'],
            template=template,
            height_frame=request.POST['height_frame'],
            json_dict_parameters=json.dumps(dict_parameters),
            fk_project=db_obj_project,
            fk_template_assignment=db_obj_template_assignment,
            fk_template_hit=db_obj_template_hit
        )
    except IntegrityError:
        messages.error(request, 'A template with this name already exists')
        return

    messages.success(request, 'Added template successfully')

def preprocess_template_inject(request, db_obj_project, html_template):
    queryset = m_Worker.objects.filter(fk_project=db_obj_project, is_blocked=True)
    list_workers = [hashlib.md5(worker.name.encode()).hexdigest() for worker in queryset]
    print(list_workers)
    if len(list_workers) == 0:
        return html_template

    print(list_workers)
    injected = ''
    injected += '''
        <script>
            var sturp = {list};
            {code_md5}
            {code_block}
        </script>
    '''.format(
        list=json.dumps(list_workers), 
        code_md5=code_shared.get_code_js_md5(), 
        code_block=code_shared.get_code_block_inject()
    )

    html_template = html_template.replace('</body>', '{}</body>'.format(injected))
    return html_template

def preprocess_template_request(request, db_obj_project, html_template):
    host = code_shared.get_url_block_worker(request) 
    path = reverse('mturk_manager:api_status_worker', kwargs={'name':db_obj_project.name, 'id_worker':'a'})[:-1]
    url = urllib.parse.urljoin(host, path)
    injected = ''
    injected += '''
        <script>
            var rkreu = '{url}';
            {code_block}
        </script>
    '''.format(
        url=url,
        code_block=code_shared.get_code_block_request(),
    )

    html_template = html_template.replace('</body>', '{}</body>'.format(injected))
    return html_template

def create_batch(db_obj_project, form, request):
    # if not code_shared.validate_form(request, [
    #     {'type':'number', 'keys':['count_assignments'], 'message': 'Invalid number of assignments'},
    #     {'type':'number', 'keys':['lifetime'], 'message': 'Invalid lifetime'},
    #     {'type':'number', 'keys':['duration'], 'message': 'Invalid duration'},
    #     {'type':'string', 'keys':['reward'], 'message': 'Invalid reward'},
    #     {'type':'string', 'keys':['title'], 'message': 'Invalid title'},
    #     {'type':'string', 'keys':['description'], 'message': 'Invalid description'},
    #     {'type':'string', 'keys':['template'], 'message': 'Invalid worker template'},
    # ]):
    #     return 

    # if not 'file_csv' in request.FILES:
    #     valid = False
    #     messages.error(request, 'Invalid csv file')
    #     return  

    print(form.cleaned_data)
    # db_obj_template = m_Template.objects.get(fk_project=db_obj_project, id=request.POST['template'])
    db_obj_template = form.cleaned_data['fk_template_main']
    if form.cleaned_data['block_workers'] == 'enabled_inject':
        db_obj_template.template = preprocess_template_inject(request, db_obj_project, db_obj_template.template)
    elif form.cleaned_data['block_workers'] == 'enabled_request':
        db_obj_template.template = preprocess_template_request(request, db_obj_project, db_obj_template.template)

    list_requirements = []

    title = form.cleaned_data['title']

    if form.cleaned_data['has_content_adult']:
        list_requirements.append({
            'QualificationTypeId': '00000000000000000060',
            'Comparator': 'EqualTo',
            'IntegerValues': [
                1,
            ],
            'RequiredToPreview': True
            # 'ActionsGuarded': 'PreviewAndAccept'
        })

        title = 'Contains adult content! {}'.format(title)

    # print(1)
    # return

    db_obj_batch = code_shared.glob_create_batch(db_obj_project, data=form.cleaned_data)
    client = code_shared.get_client(db_obj_project, form.cleaned_data['use_sandbox'])
    reader = csv.DictReader(io.StringIO(form.cleaned_data['file_csv'].read().decode('utf-8')))
    # list_entities = []
    index = 0
    for dict_parameters in reader:
        try:
            mturk_obj_hit = client.create_hit(
                Keywords=form.cleaned_data['keywords'],
                MaxAssignments=form.cleaned_data['count_assignments'],
                LifetimeInSeconds=form.cleaned_data['lifetime'],
                AssignmentDurationInSeconds=form.cleaned_data['duration'],
                AutoApprovalDelayInSeconds=1209600,
                Reward=form.cleaned_data['reward'],
                Title=title,
                Description=form.cleaned_data['description'],
                Question=code_shared.create_question(db_obj_template.template, db_obj_template.height_frame, dict_parameters),
                QualificationRequirements=list_requirements
            )
            # print(mturk_obj_hit)
        except ClientError as e:
            messages.error(request, '''
                An error occured
                <a href="#alert_1" data-toggle="collapse" class="alert-link">details</a>
                <p class="collapse mb-0" id="alert_1">
                    {}
                </p>
            '''.format(e))

            if index == 0:
                db_obj_batch.delete()

            break

        index += 1

        db_obj_tag = m_Tag.objects.create(
            name=glob_prefix_name_tag_hit+mturk_obj_hit['HIT']['HITId'],
            key_corpus=db_obj_project.name
        )

        # print(mturk_obj_hit)
        db_obj_hit = m_Hit.objects.create(
            # id_hit=str(random.randint(0, 9999999)),
            id_hit=mturk_obj_hit['HIT']['HITId'],
            fk_batch=db_obj_batch,
            parameters=json.dumps(dict_parameters),
            datetime_expiration=mturk_obj_hit['HIT']['Expiration'],
            datetime_creation=mturk_obj_hit['HIT']['CreationTime'],
        )

        # list_assignments

        # list_entities.append(db_obj_hit.id)

    db_obj_tag = m_Tag.objects.get_or_create(
        name=glob_prefix_name_tag_batch+db_obj_batch.name,
        key_corpus=db_obj_project.name
    )[0]

    messages.success(request, 'Created batch successfully')

    # m_Entity.objects.bulk_create([m_Entity(id_item=id_hit, id_item_internal=id_hit, key_corpus=db_obj_project.name) for id_hit in list_entities])
