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
    db_obj_project = m_Project.objects.prefetch_related(
        'messages_reject'
    ).get(name=name_project)

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
        Prefetch('assignments', queryset=m_Assignment.objects.prefetch_related('corpus_viewer_tags').annotate(
                count_tags_approved=Count('corpus_viewer_tags', filter=Q(corpus_viewer_tags__name='approved'), distinct=True),
                count_tags_rejected=Count('corpus_viewer_tags', filter=Q(corpus_viewer_tags__name='rejected'), distinct=True)
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
    context['db_obj_project'] = db_obj_project
    # context['queryset_messages_reject'] = m_Message_Reject.objects.filter(fk_project=db_obj_project)
    return render(request, 'mturk_manager/view.html', context)

def submit_annotations(request, db_obj_project, obj):
    client_sandbox = code_shared.get_client(db_obj_project, True)
    client_real = code_shared.get_client(db_obj_project, False)
    db_obj_tag_submitted = m_Tag.objects.get(key_corpus=db_obj_project.name, name='submitted')
    db_obj_tag_approved = m_Tag.objects.get(key_corpus=db_obj_project.name, name='approved')
    db_obj_tag_rejected = m_Tag.objects.get(key_corpus=db_obj_project.name, name='rejected')

    dict_annotations = obj['dict_assignments']
    message_reject_default = obj['message_reject_default']
    list_ids = [id_assignment for id_assignment in dict_annotations.keys()]
    for assignment in m_Assignment.objects.filter(id__in=list_ids):
        dict_annotation = dict_annotations[str(assignment.id)]

        feedback = ''
        try:
            feedback = dict_annotation['message']
        except KeyError:
            feedback = message_reject_default

        print(feedback)
        print(assignment.fk_hit.fk_batch.use_sandbox)
        client = client_sandbox if assignment.fk_hit.fk_batch.use_sandbox else client_real
        try:
            pass
            if dict_annotation['state'] == 'approve':
                response = client.approve_assignment(
                    AssignmentId=assignment.id_assignment,
                    RequesterFeedback=feedback
                )
            elif dict_annotation['state'] == 'reject':
                response = client.reject_assignment(
                    AssignmentId=assignment.id_assignment,
                    RequesterFeedback=feedback
                )
        except Exception as e:
            print(e)
            continue

        if dict_annotation['state'] == 'approve':
            db_obj_tag_submitted.corpus_viewer_items.remove(assignment)
            db_obj_tag_approved.corpus_viewer_items.add(assignment)
        elif dict_annotation['state'] == 'reject':
            db_obj_tag_submitted.corpus_viewer_items.remove(assignment)
            db_obj_tag_rejected.corpus_viewer_items.add(assignment)

    print(obj)

def normalize_answer(answer):
    dict_answer = json.loads(answer)
    normalize_answer = {}

    try:
        for value in dict_answer['QuestionFormAnswers']['Answer']:
            normalize_answer[value['QuestionIdentifier']] = value['FreeText']
    except TypeError:
        normalize_answer[dict_answer['QuestionFormAnswers']['Answer']['QuestionIdentifier']] = dict_answer['QuestionFormAnswers']['Answer']['FreeText']

    return json.dumps(normalize_answer)
