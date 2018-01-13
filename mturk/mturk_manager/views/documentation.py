from django.shortcuts import render

def documentation(request):
    context = {}
    return render(request, 'mturk_manager/documentation.html', context)