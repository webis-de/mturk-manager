from django.shortcuts import render, redirect
from mturk_manager.models import *
import urllib.parse

def index(request):

    if request.method == 'POST':
        name_project = request.POST['name_project']
        if name_project != '':
            return redirect('mturk_manager:project', name=urllib.parse.quote(name_project, safe=''))

    context = {}
    context['queryset_projects'] = m_Project.objects.all()
    return render(request, 'mturk_manager/index.html', context)