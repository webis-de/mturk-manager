from django.shortcuts import render, redirect
from mturk_manager.models import *
import urllib.parse
from mturk_manager.forms import *

def dashboard(request):
    if request.method == 'POST':
        name_project = request.POST['name_project']
        if name_project != '':
            return redirect('mturk_manager:project', name=urllib.parse.quote(name_project, safe=''))

    form = Form_Dashboard(choices=[(project.name, project.name) for project in m_Project.objects.all()])

    print(form)
    context = {}
    context['form'] = form
    context['queryset_projects'] = m_Project.objects.all()
    return render(request, 'mturk_manager/dashboard.html', context)