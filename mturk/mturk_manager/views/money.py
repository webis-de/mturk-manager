from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from mturk_manager.models import *
import urllib.parse, json, csv
from django.urls import reverse
from mturk_manager.forms import *

def money(request, name):
    name_quoted = name
    name_project = urllib.parse.unquote(name_quoted)

    if request.method == 'POST':
    	pass
        # form = Form_Open(request.POST)
        # if form.is_valid():
        #     return redirect('mturk_manager:project', name=urllib.parse.quote(form.cleaned_data['name_project'].name, safe=''))
    # else:
        # form = Form_Open()

    dict_config = {
    	'name_project': name_project,
    	'url_project': reverse('mturk_manager:project', args=[name_project]),
    	'url_api_get_balance': reverse('mturk_manager:balance', args=[name_project]),
    	'url_api_assignments_real_approved': reverse('mturk_manager:api_assignments_real_approved_tmp', args=[name_project]),
    }

    context = {}
    context['json_config'] = json.dumps(dict_config)
        
    return render(request, 'mturk_manager/money.html', context)