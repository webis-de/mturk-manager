from django.shortcuts import render, redirect
# from mturk_manager.views import code_shared
# from mturk_manager.models import *
# from viewer.models import *
import json
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
import urllib.parse
import time
from django.db.models import Prefetch, Count, When, BooleanField, Case, Q
from django.contrib import messages
# from mturk_manager.classes import Manager_Global_DB
from django.middleware.csrf import get_token
from django.conf import settings as settings_django

def get_url_absolute(path='', use_sandbox=True):
    url = ''
    if path.startswith('/'):
        url = settings_django.URL_GLOBAL_DB + path
    else:
        url = settings_django.URL_GLOBAL_DB + '/' + path

    if not use_sandbox:
        url += '?use_sandbox=false'

    return url

def view(request, name):
    placeholder_slug_project = 'PLACEHOLDER_SLUG_PROJECT'
    list_ids = json.loads(request.GET.get('list_ids', '[]'))

    context = {
        'token_instance': settings_django.TOKEN_INSTANCE,
        'token_csrf': get_token(request),
        'url_api_project':  get_url_absolute('projects/{}'.format(placeholder_slug_project)),
        'url_api_assignments':  get_url_absolute('projects/{}/assignments'.format(placeholder_slug_project)),
        'url_api_hits':  get_url_absolute('projects/{}/hits'.format(placeholder_slug_project)),
        'url_api_batches':  get_url_absolute('projects/{}/batches_for_annotation'.format(placeholder_slug_project)),
        'url_api_workers':  get_url_absolute('projects/{}/workers'.format(placeholder_slug_project)),
        'url_api_messages_reject':  get_url_absolute('api/messages_reject'.format(placeholder_slug_project)),
        
        'slug_project': name,
        'list_ids': list_ids,
    }
    context['context'] = json.dumps(context)

    return render(request, 'mturk_manager/view.html', context=context)
    ############
    context = {}
    name_quoted = name
    name_project = urllib.parse.unquote(name_quoted)
    db_obj_project = m_Project.objects.prefetch_related(
        'messages_reject'
    ).get(name=name_project)

    if not code_shared.is_project_up_to_date(request, db_obj_project, name_project):    
        return redirect('mturk_manager:index')

    try:
        list_ids = json.loads(request.GET['list_ids'])
    except (KeyError, json.JSONDecodeError):
        messages.error(request, 'Please provide valid assignments')
        return redirect('mturk_manager:project', name=name_quoted)
    if len(list_ids) == 0:
        messages.error(request, 'Please provide assignments')
        return redirect('mturk_manager:project', name=name_quoted)

    if request.method == 'POST':
        obj = json.loads(request.body.decode("utf-8"))

        if obj['task'] == 'submit_annotations':
            submit_annotations(request, db_obj_project, obj)

        return HttpResponseRedirect(reverse('mturk_manager:view', args=[name_quoted])+ '?list_ids='+request.GET['list_ids'])

    queryset_hits = m_Hit.objects.filter(
        assignments__id__in=list_ids
    ).select_related(
        'fk_batch__fk_template__fk_template_assignment',
        'fk_batch__fk_template__fk_template_hit',
    ).prefetch_related(
        Prefetch('assignments', queryset=m_Assignment.objects.prefetch_related('corpus_viewer_tags').filter(
                id__in=list_ids
            ).annotate(
                count_tags_approved=Count('corpus_viewer_tags', filter=Q(corpus_viewer_tags__name='approved'), distinct=True),
                count_tags_rejected=Count('corpus_viewer_tags', filter=Q(corpus_viewer_tags__name='rejected'), distinct=True),
                count_tags_rejected_externally=Count('corpus_viewer_tags', filter=Q(corpus_viewer_tags__name='rejected externally'), distinct=True),
                count_tags_approved_externally=Count('corpus_viewer_tags', filter=Q(corpus_viewer_tags__name='approved externally'), distinct=True),
            ).distinct()
            ,to_attr='list_assignments'
        )
    ).distinct()

    for hit in queryset_hits:
        # for assignment in hit.assignments.all():
        for assignment in hit.list_assignments:
            # print(assignment.is_approved1)
            assignment.answer_normalized = normalize_answer(assignment.answer)
            if assignment.count_tags_approved_externally == 1:
                assignment.state = 'approved_externally'
            elif assignment.count_tags_rejected_externally == 1:
                assignment.state = 'rejected_externally'
            elif assignment.count_tags_approved == 1:
                assignment.state = 'approved'
            elif assignment.count_tags_rejected == 1:
                assignment.state = 'rejected'
            else:
                assignment.state = 'submitted'


            assignment.info_worker = json.dumps(get_info_worker(assignment))

    context['queryset_hits'] = queryset_hits
    context['name_project'] = name_project
    context['db_obj_project'] = db_obj_project
    # context['queryset_messages_reject'] = m_Message_Reject.objects.filter(fk_project=db_obj_project)
    return render(request, 'mturk_manager/view.html', context)

def get_info_worker(db_obj_assignment):
    dict_result = {} 

    db_obj_batch = db_obj_assignment.fk_hit.fk_batch
    db_obj_worker = db_obj_assignment.fk_worker

    count_assignments_submitted = 0
    count_assignments_approved = 0
    count_assignments_rejected = 0
    # get all assignments from this worker from this batch
    for assignment in m_Assignment.objects.prefetch_related('corpus_viewer_tags').filter(
        fk_worker=db_obj_worker,
        fk_hit__fk_batch=db_obj_batch
    ).annotate(
        count_tags_approved=Count('corpus_viewer_tags', filter=Q(corpus_viewer_tags__name='approved'), distinct=True),
        count_tags_rejected=Count('corpus_viewer_tags', filter=Q(corpus_viewer_tags__name='rejected'), distinct=True),
        count_tags_rejected_externally=Count('corpus_viewer_tags', filter=Q(corpus_viewer_tags__name='rejected externally'), distinct=True),
        count_tags_approved_externally=Count('corpus_viewer_tags', filter=Q(corpus_viewer_tags__name='approved externally'), distinct=True),
    ).distinct():
            if assignment.id == db_obj_assignment.id:
                continue


            if assignment.count_tags_approved_externally == 1:
                count_assignments_rejected += 1
            elif assignment.count_tags_rejected_externally == 1:
                count_assignments_approved += 1
            elif assignment.count_tags_approved == 1:
                count_assignments_approved += 1
            elif assignment.count_tags_rejected == 1:
                count_assignments_rejected += 1
            else:
                count_assignments_submitted += 1

    dict_result["id_worker"] = db_obj_worker.name
    dict_result["count_assignments_submitted"] = count_assignments_submitted
    dict_result["count_assignments_approved"] = count_assignments_approved
    dict_result["count_assignments_rejected"] = count_assignments_rejected

    return dict_result

def submit_annotations(request, db_obj_project, obj):
    client_sandbox = code_shared.get_client(db_obj_project, True)
    client_real = code_shared.get_client(db_obj_project, False)
    db_obj_tag_submitted = m_Tag.objects.get(key_corpus=db_obj_project.name, name='submitted')
    db_obj_tag_approved = m_Tag.objects.get(key_corpus=db_obj_project.name, name='approved')
    db_obj_tag_rejected = m_Tag.objects.get(key_corpus=db_obj_project.name, name='rejected')
    db_obj_tag_rejected_externally = m_Tag.objects.get(key_corpus=db_obj_project.name, name='rejected externally')
    db_obj_tag_approved_externally = m_Tag.objects.get(key_corpus=db_obj_project.name, name='approved externally')

    dict_annotations = obj['dict_assignments']
    softblock_on_reject = obj['softblock_on_reject']
    extend_hit_on_reject = obj['extend_hit_on_reject']
    message_reject_default = obj['message_reject_default']
    list_ids = [id_assignment for id_assignment in dict_annotations.keys()]
    for assignment in m_Assignment.objects.filter(id__in=list_ids):
        dict_annotation = dict_annotations[str(assignment.id)]

        feedback = ''
        try:
            feedback = dict_annotation['message']
        except KeyError:
            feedback = message_reject_default

        client = client_sandbox if assignment.fk_hit.fk_batch.use_sandbox else client_real
        try:
            pass
            if dict_annotation['state'] == 'approve' or dict_annotation['state'] == 'reject_internally':
                response = client.approve_assignment(
                    AssignmentId=assignment.id_assignment,
                    RequesterFeedback=feedback
                )
            elif dict_annotation['state'] == 'reject' or dict_annotation['state'] == 'approve_internally':
                response = client.reject_assignment(
                    AssignmentId=assignment.id_assignment,
                    RequesterFeedback=feedback
                )

            print(response)
        except Exception as e:
            print(e)
            continue


        if dict_annotation['state'] == 'reject' or dict_annotation['state'] == 'approve_internally':
            if extend_hit_on_reject == True:
                create_additional_assignment_for_hit(assignment.fk_hit, client)

        if dict_annotation['state'] == 'reject' or dict_annotation['state'] == 'approve_internally' or dict_annotation['state'] == 'reject_internally':
            if softblock_on_reject == True:
                softblock_worker(assignment.fk_worker, client)



        db_obj_tag_submitted.corpus_viewer_items.remove(assignment)
        if dict_annotation['state'] == 'approve':
            db_obj_tag_approved.corpus_viewer_items.add(assignment)
        elif dict_annotation['state'] == 'reject':
            db_obj_tag_rejected.corpus_viewer_items.add(assignment)
        elif dict_annotation['state'] == 'reject_internally':
            db_obj_tag_rejected.corpus_viewer_items.add(assignment)
            db_obj_tag_approved_externally.corpus_viewer_items.add(assignment)
        elif dict_annotation['state'] == 'approve_internally':
            db_obj_tag_approved.corpus_viewer_items.add(assignment)
            db_obj_tag_rejected_externally.corpus_viewer_items.add(assignment)

    print(obj)

def softblock_worker(db_obj_worker, client):
    # response = client.create_worker_block(
    #     WorkerId=db_obj_worker.name,
    #     Reason='blocked because recject',
    # )

    # print(response)

    db_obj_worker.is_blocked = True
    db_obj_worker.save()

def create_additional_assignment_for_hit(db_obj_hit, client):
    response = client.create_additional_assignments_for_hit(
        HITId=db_obj_hit.id_hit,
        NumberOfAdditionalAssignments=1
    )
    print(response)

    response = client.update_expiration_for_hit(
        HITId=db_obj_hit.id_hit,
        NumberOfAdditionalAssignments=1
    )
    print(response)

    db_obj_hit.count_assignments_additional = db_obj_hit.count_assignments_additional * 1
    db_obj_hit.save()




def normalize_answer(answer):
    dict_answer = json.loads(answer)
    normalize_answer = {}

    try:
        for value in dict_answer['QuestionFormAnswers']['Answer']:
            normalize_answer[value['QuestionIdentifier']] = value['FreeText']
    except TypeError:
        normalize_answer[dict_answer['QuestionFormAnswers']['Answer']['QuestionIdentifier']] = dict_answer['QuestionFormAnswers']['Answer']['FreeText']

    return json.dumps(normalize_answer)
