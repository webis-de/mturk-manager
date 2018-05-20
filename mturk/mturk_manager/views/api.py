import urllib.parse
from django.http import JsonResponse
from mturk_manager.models import *
from viewer.models import *
from mturk_manager.views import code_shared
import json

def balance(request, name):
    name_quoted = name
    name_project = urllib.parse.unquote(name_quoted)
    db_obj_project = m_Project.objects.get(
        name=name_project
    )
    return JsonResponse({
        'balance': code_shared.get_client(db_obj_project, use_sandbox=False).get_account_balance()['AvailableBalance']
    })

def api(request, name):
    name_quoted = name
    name_project = urllib.parse.unquote(name_quoted)
    db_obj_project = m_Project.objects.get(
        name=name_project
    )

    if request.method == 'POST':
        if request.POST['task'] == 'unblock_workers':
            unblock_workers(request, db_obj_project)
        elif request.POST['task'] == 'block_workers':
            block_workers(request, db_obj_project)
        elif request.POST['task'] == 'approve_assignments_selected':
            approve_assignments_selected(request, db_obj_project)
            block_workers(request, db_obj_project)
        elif request.POST['task'] == 'reject_assignments_selected':
            reject_assignments_selected(request, db_obj_project)

    return JsonResponse({})

def api_assignments_real_approved_for_batch(request, name, name_batch):
    dict_result = {}

    queryset = m_Assignment.objects.filter(
        fk_hit__fk_batch__fk_project__name=name,
        fk_hit__fk_batch__use_sandbox=False,
        corpus_viewer_tags__name='approved',
        fk_hit__fk_batch__name=name_batch,
    )

    list_assignments = [assignment.id_assignment for assignment in queryset]

    dict_result['success'] = True
    dict_result['assignments'] = list_assignments
    dict_result['count_assignments'] = len(list_assignments)
    return JsonResponse(dict_result)

def api_assignments_real_approved(request, name):
    dict_result = {}
 
    queryset = m_Assignment.objects.filter(
        fk_hit__fk_batch__fk_project__name=name,
        fk_hit__fk_batch__use_sandbox=False,
        corpus_viewer_tags__name='approved'
    )

    list_assignments = [assignment.id_assignment for assignment in queryset]

    dict_result['success'] = True
    dict_result['assignments'] = list_assignments
    dict_result['count_assignments'] = len(list_assignments)
    return JsonResponse(dict_result)

def api_assignment(request, name, id_assignment):
    dict_result = {}
 
    obj_db_assignment = m_Assignment.objects.get(
        id_assignment=id_assignment
    )


    dict_result['success'] = True
    dict_result['answer'] = obj_db_assignment.answer
    return JsonResponse(dict_result)

def api_assignments_real(request, name):
    dict_result = {}
 
    queryset = m_Assignment.objects.filter(
        fk_hit__fk_batch__fk_project__name=name,
        fk_hit__fk_batch__use_sandbox=False,
    )

    list_assignments = [assignment.id_assignment for assignment in queryset]

    dict_result['success'] = True
    dict_result['assignments'] = list_assignments
    dict_result['count_assignments'] = len(list_assignments)
    return JsonResponse(dict_result)

def api_assignments_fake(request, name):
    dict_result = {}
 
    queryset = m_Assignment.objects.filter(
        fk_hit__fk_batch__fk_project__name=name,
        fk_hit__fk_batch__use_sandbox=True,
    )

    list_assignments = [assignment.id_assignment for assignment in queryset]

    dict_result['success'] = True
    dict_result['assignments'] = list_assignments
    dict_result['count_assignments'] = len(list_assignments)
    return JsonResponse(dict_result)

def api_workers(request, name):
    dict_result = {}
 
    queryset = m_Worker.objects.filter(
        assignments__fk_hit__fk_batch__fk_project__name=name,
        assignments__fk_hit__fk_batch__use_sandbox=False,
    )

    list_workers = [worker.name for worker in queryset]

    dict_result['success'] = True
    dict_result['workers'] = list_workers
    dict_result['count_workers'] = len(list_workers)
    return JsonResponse(dict_result)

def api_status_worker(request, name, id_worker):
    dict_result = {} 

    try:
        db_obj_worker = m_Worker.objects.get(name=id_worker, fk_project__name=name)
    except m_Worker.DoesNotExist:
        dict_result['success'] = False
    else:
        dict_result['success'] = True
        dict_result['blocked'] = db_obj_worker.is_blocked
    finally:
        response_json = JsonResponse(dict_result)
        response_json['Access-Control-Allow-Origin'] = '*'
        return response_json

def approve_assignments_selected(request, db_obj_project):
    list_ids = request.POST.getlist('list_ids[]')
    
    db_obj_tag_submitted = m_Tag.objects.get(key_corpus=db_obj_project.name, name='submitted')
    db_obj_tag_approved = m_Tag.objects.get(key_corpus=db_obj_project.name, name='approved')
    db_obj_tag_rejected = m_Tag.objects.get(key_corpus=db_obj_project.name, name='rejected')
    
    for assignment in m_Assignment.objects.filter(id__in=list_ids):
        db_obj_tag_submitted.corpus_viewer_items.remove(assignment)
        db_obj_tag_rejected.corpus_viewer_items.remove(assignment)
        db_obj_tag_approved.corpus_viewer_items.add(assignment)

def reject_assignments_selected(request, db_obj_project):
    list_ids = request.POST.getlist('list_ids[]')
    
    db_obj_tag_submitted = m_Tag.objects.get(key_corpus=db_obj_project.name, name='submitted')
    db_obj_tag_approved = m_Tag.objects.get(key_corpus=db_obj_project.name, name='approved')
    db_obj_tag_rejected = m_Tag.objects.get(key_corpus=db_obj_project.name, name='rejected')
    
    for assignment in m_Assignment.objects.filter(id__in=list_ids):
        db_obj_tag_submitted.corpus_viewer_items.remove(assignment)
        db_obj_tag_approved.corpus_viewer_items.remove(assignment)
        db_obj_tag_rejected.corpus_viewer_items.add(assignment)

def unblock_workers(request, db_obj_project):
    list_ids = request.POST.getlist('list_ids[]')

    m_Worker.objects.filter(
        fk_project=db_obj_project,
        id__in=list_ids
    ).update(is_blocked=False)

def block_workers(request, db_obj_project):
    list_ids = request.POST.getlist('list_ids[]')

    m_Worker.objects.filter(
        fk_project=db_obj_project,
        id__in=list_ids
    ).update(is_blocked=True)