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