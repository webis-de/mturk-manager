from django.shortcuts import render, redirect
from mturk_manager.models import *
import urllib.parse

def create(request):
    context = {}
    context['queryset_account_mturk'] = m_Account_Mturk.objects.all()

    if request.method == 'POST':
        print(request.POST)
        print(request.FILES)
        verified_input = verify_input(request)
        if not verified_input == True:
            context['success'] = False
            return render(request, 'mturk_manager/create.html', context)
            
        create_project(request)

        context['success'] = True
        return redirect('mturk_manager:project', name=urllib.parse.quote(request.POST['name'], safe=''), permanent=True)
    

    return render(request, 'mturk_manager/create.html', context)

def create_project(request):
    template = None
    if request.POST['html_template'].strip() == '':
        if request.FILES['file_template'].charset == None:
            template = request.FILES['file_template'].read().decode('utf-8')
        else:
            template = request.FILES['file_template'].read().decode(request.FILES['file_template'].charset)

    else:
        template = request.POST['html_template']

    db_obj_account_mturk = m_Account_Mturk.objects.get(name=request.POST['name_account_mturk'])

    m_Project.objects.get_or_create(
        name=request.POST['name'],
        template = template,
        fk_account_mturk = db_obj_account_mturk,
    )

def verify_input(request):
    try:
        if request.POST['name'].strip() == '':
            return False

        if request.POST['html_template'].strip() == '':
            if 'file_template' not in request.FILES:
                return False

    except KeyError:
        return False

    return True