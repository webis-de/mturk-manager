from django.shortcuts import render, redirect
from mturk_manager.models import *
import urllib.parse

def settings(request):
    context = {}

    if request.method == 'POST':
        print(request.POST)
        verified_input = verify_input(request)
        if not verified_input == True:
            context['success'] = False
            context['queryset_mturk'] = m_MTurk.objects.all()
            return render(request, 'mturk_manager/settings.html', context)

        create_account(request)

        context['success'] = True
        return redirect('mturk_manager:settings', permanent=True)

    context['queryset_mturk'] = m_MTurk.objects.all()

    return render(request, 'mturk_manager/settings.html', context)

def create_account(request):
    m_MTurk.objects.get_or_create(
        name = request.POST['name'],
        key_access = request.POST['key_access'],
        key_secret = request.POST['key_secret'],
    )


def verify_input(request):
    if request.POST['name'].strip() == '':
        return False
    if request.POST['key_access'].strip() == '':
        return False
    if request.POST['key_secret'].strip() == '':
        return False

    return True