from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from mturk_manager.models import *
import urllib.parse, json, csv
from django.urls import reverse
from mturk_manager.forms import *
from django.middleware.csrf import get_token

def money(request, name):
    name_quoted = name
    slug_project = urllib.parse.unquote(name_quoted)

    if request.method == 'POST':
    	pass
        # form = Form_Open(request.POST)
        # if form.is_valid():
        #     return redirect('mturk_manager:project', name=urllib.parse.quote(form.cleaned_data['name_project'].name, safe=''))
    # else:
        # form = Form_Open()
    dict_config = {
        'slug_project_current': slug_project,
    	'token_csrf': get_token(request),
        'url_project': reverse('mturk_manager:project', args=[slug_project]),
        'url_api_get_balance': reverse('mturk_manager:balance', args=[slug_project]),
        'url_api_assignments_real_approved': reverse('mturk_manager:api_assignments_real_approved_tmp', args=[slug_project]),
        'url_api_qualifications': reverse('mturk_manager:qualifications_for_project', args=[slug_project]),
        # 'url_api_qualification': reverse('mturk_manager:qualification_for_project', args=[slug_project, 'da']),
        'url_api_workers': reverse('mturk_manager:workers_for_project', args=[slug_project]),
        'url_api_status_block': reverse('mturk_manager:workers_for_project_status_block', args=[slug_project]),
        
        'url_api_projects': reverse('mturk_manager:projects'),

        'url_api_batches': reverse('mturk_manager:batches_for_project', args=[slug_project]),
        # 'url_api_project': reverse('mturk_manager:project_api_tmp'),
    }

    context = {}
    context['json_config'] = json.dumps(dict_config)
        
    return render(request, 'mturk_manager/money.html', context)