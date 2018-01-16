from django.shortcuts import render, redirect
from mturk_manager.views import code_shared
from mturk_manager.models import *
from viewer.models import *
import json
from django.http import HttpResponseRedirect
from django.urls import reverse
import urllib.parse
import time
from django.db.models import Prefetch, Count, When, BooleanField, Case, Q
from django.contrib import messages

def view(request, name):
    context = {}
    name_quoted = name
    name_project = urllib.parse.unquote(name_quoted)
    db_obj_project = m_Project.objects.get(name=name_project)

    try:
        list_ids = json.loads(request.GET['list_ids'])
    except (KeyError, json.JSONDecodeError):
        messages.error(request, 'Please provide valid assignments')
        return redirect('mturk_manager:project', name=name_quoted, permanent=True)
    if len(list_ids) == 0:
        messages.error(request, 'Please provide assignments')
        return redirect('mturk_manager:project', name=name_quoted, permanent=True)


    if request.method == 'POST':
        if request.POST['task'] == 'button_mturk_approve_selected':
            list_ids = request.POST.getlist('checkbox_assignment')
            approve_assignments(request, db_obj_project, list_ids)
        if request.POST['task'] == 'button_mturk_reject_selected':
            list_ids = request.POST.getlist('checkbox_assignment')
            reject_assignments(request, db_obj_project, list_ids)
        if request.POST['task'].startswith('button_mturk_approve__'):
            id_assignment = request.POST['task'].split('__')[1]
            approve_assignments(request, db_obj_project, [id_assignment])
        if request.POST['task'].startswith('button_mturk_reject__'):
            id_assignment = request.POST['task'].split('__')[1]
            reject_assignments(request, db_obj_project, [id_assignment])

        return HttpResponseRedirect(reverse('mturk_manager:view', args=[name_quoted])+ '?list_ids='+request.GET['list_ids'])

    queryset_hits = m_Hit.objects.filter(
        assignments__id__in=list_ids
    ).select_related(
        'fk_batch__fk_template__fk_template_assignment',
        'fk_batch__fk_template__fk_template_hit',
    ).prefetch_related(
        Prefetch('assignments', queryset=m_Assignment.objects.prefetch_related('tags').annotate(
                count_tags_approved=Count('tags', filter=Q(tags__name='approved'), distinct=True),
                count_tags_rejected=Count('tags', filter=Q(tags__name='rejected'), distinct=True)
            ).distinct()
            ,to_attr='list_assignments'
        )
    ).distinct()

    for hit in queryset_hits:
        # for assignment in hit.assignments.all():
        for assignment in hit.list_assignments:
            # print(assignment.is_approved1)
            assignment.answer_normalized = normalize_answer(assignment.answer)
            assignment.is_approved = False if assignment.count_tags_approved == 0 else True
            assignment.is_rejected = False if assignment.count_tags_rejected == 0 else True

    context['queryset_hits'] = queryset_hits
    context['name_project'] = name_project
    context['queryset_messages_reject'] = m_Message_Reject.objects.filter(fk_project=db_obj_project)
    return render(request, 'mturk_manager/view.html', context)

def approve_assignments(request, db_obj_project, list_ids):
    client_sandbox = code_shared.get_client(db_obj_project, True)
    client = code_shared.get_client(db_obj_project, False)
    db_obj_tag_submitted = m_Tag.objects.get(key_corpus=db_obj_project.name, name='submitted')
    db_obj_tag_approved = m_Tag.objects.get(key_corpus=db_obj_project.name, name='approved')

    list_success = []
    list_fail = []

    for assignment in m_Assignment.objects.filter(id__in=list_ids, fk_hit__fk_batch__use_sandbox=True):
        try:
            response = client_sandbox.approve_assignment(
                AssignmentId=assignment.id_assignment
            )
        except Exception as e:
            list_fail.append(assignment)
            continue

        db_obj_tag_submitted.items.remove(assignment)
        db_obj_tag_approved.items.add(assignment)

        list_success.append(assignment)

    for assignment in m_Assignment.objects.filter(id__in=list_ids, fk_hit__fk_batch__use_sandbox=False):
        try:
            response = client.approve_assignment(
                AssignmentId=assignment.id_assignment
            )
        except Exception as e:
            list_fail.append(assignment)
            continue

        db_obj_tag_submitted.items.remove(assignment)
        db_obj_tag_approved.items.add(assignment)

        list_success.append(assignment)

    if len(list_success) != 0:
        messages.success(request, 'Approved {} assignment(s)'.format(len(list_success)))
    if len(list_fail) != 0:
        messages.error(request, 'Failed to approve {} assignment(s)'.format(len(list_fail)))

def reject_assignments(request, db_obj_project, list_ids):
    client_sandbox = code_shared.get_client(db_obj_project, True)
    client = code_shared.get_client(db_obj_project, False)
    db_obj_tag_submitted = m_Tag.objects.get(key_corpus=db_obj_project.name, name='submitted')
    db_obj_tag_rejected = m_Tag.objects.get(key_corpus=db_obj_project.name, name='rejected')

    list_success = []
    list_fail = []

    for assignment in m_Assignment.objects.filter(id__in=list_ids, fk_hit__fk_batch__use_sandbox=True):
        try:
            response = client_sandbox.reject_assignment(
                AssignmentId=assignment.id_assignment,
                RequesterFeedback=''
            )
        except Exception as e:
            print(e)
            list_fail.append(assignment)
            continue

        db_obj_tag_submitted.items.remove(assignment)
        db_obj_tag_rejected.items.add(assignment)

        list_success.append(assignment)

    for assignment in m_Assignment.objects.filter(id__in=list_ids, fk_hit__fk_batch__use_sandbox=False):
        try:
            response = client.reject_assignment(
                AssignmentId=assignment.id_assignment,
                RequesterFeedback=''
            )
        except Exception as e:
            print(e)
            list_fail.append(assignment)
            continue

        db_obj_tag_submitted.items.remove(assignment)
        db_obj_tag_rejected.items.add(assignment)

        list_success.append(assignment)


    if len(list_success) != 0:
        messages.success(request, 'Rejected {} assignment(s)'.format(len(list_success)))
    if len(list_fail) != 0:
        messages.error(request, 'Failed to reject {} assignment(s)'.format(len(list_fail)))

def normalize_answer(answer):
    dict_answer = json.loads(answer)
    normalize_answer = {}

    try:
        for value in dict_answer['QuestionFormAnswers']['Answer']:
            normalize_answer[value['QuestionIdentifier']] = value['FreeText']
    except TypeError:
        normalize_answer[dict_answer['QuestionFormAnswers']['Answer']['QuestionIdentifier']] = dict_answer['QuestionFormAnswers']['Answer']['FreeText']

    return json.dumps(normalize_answer)
