import urllib.parse
from django.http import JsonResponse
from mturk_manager.models import *
import json

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

    return JsonResponse({})

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
        return JsonResponse(dict_result)

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