from django.shortcuts import render, redirect
from mturk_manager.views import code_shared
from mturk_manager.models import *
from viewer.models import *
import json
from django.http import HttpResponseRedirect
from django.urls import reverse
import urllib.parse
import time
from django.db.models import Prefetch, Count, When, BooleanField, Case
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
        Prefetch('assignments', queryset=m_Assignment.objects.select_related(
            'fk_entity'
            ).prefetch_related('fk_entity__viewer_tags')
            ,to_attr='list_assignments'
        )
    ).distinct()

    for hit in queryset_hits:
        for assignment in hit.list_assignments:
            assignment.answer_normalized = normalize_answer(assignment.answer)
            set_tags = {tag.name for tag in assignment.fk_entity.viewer_tags.all()}
            assignment.is_approved = 'approved' in set_tags
            assignment.is_rejected = 'rejected' in set_tags

    context['queryset_hits'] = queryset_hits
    context['name_project'] = name_project
    return render(request, 'mturk_manager/view.html', context)

def approve_assignments(request, db_obj_project, list_ids):
    client = code_shared.get_client(db_obj_project)
    db_obj_tag_submitted = m_Tag.objects.get(key_corpus=db_obj_project.name, name='submitted')
    db_obj_tag_approved = m_Tag.objects.get(key_corpus=db_obj_project.name, name='approved')

    dict_entites = {entity.id_item_internal: entity for entity in m_Entity.objects.filter(id_item_internal__in=list_ids)}

    list_success = []
    list_fail = []

    for assignment in m_Assignment.objects.filter(id__in=list_ids):
        try:
            response = client.approve_assignment(
                AssignmentId=assignment.id_assignment
            )
        except Exception as e:
            list_fail.append(assignment)
            continue

        db_obj_entity = dict_entites[assignment.id]
        db_obj_tag_submitted.m2m_entity.remove(db_obj_entity)
        db_obj_tag_approved.m2m_entity.add(db_obj_entity)

        list_success.append(assignment)

    if len(list_success) != 0:
        messages.success(request, 'Approved {} assignment(s)'.format(len(list_success)))
    if len(list_fail) != 0:
        messages.error(request, 'Failed to approve {} assignment(s)'.format(len(list_fail)))

def reject_assignments(request, db_obj_project, list_ids):
    client = code_shared.get_client(db_obj_project)
    db_obj_tag_submitted = m_Tag.objects.get(key_corpus=db_obj_project.name, name='submitted')
    db_obj_tag_rejected = m_Tag.objects.get(key_corpus=db_obj_project.name, name='rejected')

    dict_entites = {entity.id_item_internal: entity for entity in m_Entity.objects.filter(id_item_internal__in=list_ids)}

    list_success = []
    list_fail = []

    for assignment in m_Assignment.objects.filter(id__in=list_ids):
        try:
            response = client.reject_assignment(
                AssignmentId=assignment.id_assignment,
                RequesterFeedback=''
            )
        except Exception as e:
            print(e)
            list_fail.append(assignment)
            continue

        db_obj_entity = dict_entites[assignment.id]
        db_obj_tag_submitted.m2m_entity.remove(db_obj_entity)
        db_obj_tag_rejected.m2m_entity.add(db_obj_entity)

        list_success.append(assignment)


    if len(list_success) != 0:
        messages.success(request, 'Rejected {} assignment(s)'.format(len(list_success)))
    if len(list_fail) != 0:
        messages.error(request, 'Failed to reject {} assignment(s)'.format(len(list_fail)))

def normalize_answer(answer):
    dict_answer = json.loads(answer)
    normalize_answer = {}

    for value in dict_answer['QuestionFormAnswers']['Answer']:
        normalize_answer[value['QuestionIdentifier']] = value['FreeText']

    return json.dumps(normalize_answer)
