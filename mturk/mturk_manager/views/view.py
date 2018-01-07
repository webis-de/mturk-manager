from django.shortcuts import render, redirect
import json

def view(request, name):
    context = {}

    list_ids = json.loads(request.GET['list_ids'])
    print(list_ids)
    # context['queryset_account_mturk'] = m_Account_Mturk.objects.all()

    # if request.method == 'POST':
    #     print(request.COOKIES)
    #     print(request.POST)
    #     print(request.FILES)
    #     if not verify_input(request) == True:
    #         context['success'] = False
    #         return render(request, 'mturk_manager/create.html', context)
            
    #     create_project(request)

    #     context['success'] = True
    #     return redirect('mturk_manager:project', name=urllib.parse.quote(request.POST['name'], safe=''), permanent=True)
    

    return render(request, 'mturk_manager/view.html', context)