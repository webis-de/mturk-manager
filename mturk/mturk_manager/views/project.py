from django.shortcuts import render, redirect
from mturk_manager.models import *
import urllib.parse

def project(request, name):
    context = {}
    name = urllib.parse.unquote(name)
    db_obj_project = m_Project.objects.get(name=name)

    if request.method == 'POST':
    	pass
    	
    context['db_obj_project'] = db_obj_project
    return render(request, 'mturk_manager/project.html', context)