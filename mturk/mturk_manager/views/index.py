from django.shortcuts import render, redirect
from mturk_manager.models import *
import urllib.parse
from mturk_manager.forms import *

def dashboard(request):
    if request.method == 'POST':
        form = Form_Open(request.POST)
        if form.is_valid():
            return redirect('mturk_manager:project', name=form.cleaned_data['name_project'].slug)
            # return redirect('mturk_manager:project', name=urllib.parse.quote(form.cleaned_data['name_project'].slug, safe=''))
    else:
        form = Form_Open()
        
    return render(request, 'mturk_manager/dashboard.html', {'form': form})