from django.shortcuts import render, redirect
from mturk_manager.models import *
import json
import urllib.parse
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


    # print(list_ids)
    # context['queryset_account_mturk'] = m_Account_Mturk.objects.all()
    for assignment in m_Assignment.objects.filter(
        fk_hit__fk_batch__fk_project=db_obj_project, 
        id__in=list_ids
    ).select_related('fk_hit__fk_batch__fk_template__fk_template_assignment'):
        print(assignment.fk_hit.id_hit)
        print(assignment.fk_hit.fk_batch.fk_template.fk_template_assignment.template)
    # if request.method == 'POST':
    #     print(request.COOKIES)
    #     print(request.POST)
    #     print(request.FILES)
    #     if not verify_input(request) == True:
    #         context['success'] = False
    #         return render(request, 'mturk_manager/create.html', context)
            
    #     create_project(request)

    #     context['success'] = True
    #     return redirect('mturk_manager:project', name=urllib.parse.quote(request.POST['name'], safe=''), permanent=True)
    

    return render(request, 'mturk_manager/view.html', context)