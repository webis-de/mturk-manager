from django.shortcuts import render, redirect
from mturk_manager.models import *
import urllib.parse
from django.contrib import messages

def settings(request):
    context = {}

    if request.method == 'POST':
        if request.POST['task'] == 'add_account':
            add_account(request)
        if request.POST['task'] == 'update_account':
            update_account(request)
        return redirect('mturk_manager:settings', permanent=True)

    context['queryset_mturk'] = m_Account_Mturk.objects.all()

    return render(request, 'mturk_manager/settings.html', context)


def update_account(request):
    if not verify_input_add_account(request):
        return 

    m_Account_Mturk.objects.filter(
        id=request.POST['id']
    ).update(
        name = request.POST['name'],
        key_access = request.POST['key_access'],
        key_secret = request.POST['key_secret'],
    )   

    messages.success(request, 'Updated account successfully')

def add_account(request):
    if not verify_input_add_account(request):
        return 

    m_Account_Mturk.objects.get_or_create(
        name = request.POST['name'],
        key_access = request.POST['key_access'],
        key_secret = request.POST['key_secret'],
    )

    messages.success(request, 'Created account successfully')

def verify_input_add_account(request):
    valid = True
    list_messages = []

    try:
        if request.POST['name'].strip() == '':
            valid = False
            list_messages.append('Invalid name')
        if request.POST['key_access'].strip() == '':
            valid = False
            list_messages.append('Invalid access key')
        if request.POST['key_secret'].strip() == '':
            valid = False
            list_messages.append('Invalid secret key')
    except KeyError:
        list_messages.append('Unexpected error, please cry')
        valid = False

    for message in list_messages:
        messages.error(request, message)

    return valid