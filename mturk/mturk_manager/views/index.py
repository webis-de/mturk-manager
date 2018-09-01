from django.shortcuts import render, redirect
from mturk_manager.models import *
import urllib.parse
from mturk_manager.forms import *
from mturk_manager.views import code_shared

def dashboard(request):
    if request.method == 'POST':
        form = Form_Open(request.POST)
        if form.is_valid():
            return redirect('mturk_manager:project', slug_project=form.cleaned_data['name_project'].slug)
            # return redirect('mturk_manager:project', name=urllib.parse.quote(form.cleaned_data['name_project'].slug, safe=''))
    else:
        form = Form_Open()

    client = code_shared.get_client(m_Project.objects.first(), use_sandbox=False)
    response = client.list_hits(
        MaxResults=100
    )

    # for x in range(2):
    #     response = client.list_hits(
    #         MaxResults=100,
    #         NextToken=response['NextToken'],
    #     )

    for index, hit in enumerate(response['HITs']):
        print(index, hit['CreationTime'])
        # print(hit['QualificationRequirements'])

    return render(request, 'mturk_manager/dashboard.html', {'form': form})