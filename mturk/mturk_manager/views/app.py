from django.shortcuts import render, redirect
from django.urls import reverse
import json
# from mturk_manager.models import *
# import urllib.parse
# from mturk_manager.views import code_shared
from django.middleware.csrf import get_token
from mturk_manager.classes import Manager_Global_DB

def app(request):
    placeholder_slug_project = 'PLACEHOLDER_SLUG_PROJECT'

    dict_config = {
        'token_instance': Manager_Global_DB.object_global_db.token_instance,
        'token_csrf': get_token(request),
        # 'url_project': reverse('mturk_manager:project', args=[placeholder_slug_project]),
        # 'url_api_get_balance': reverse('mturk_manager:balance', args=[placeholder_slug_project]),
        # 'url_api_assignments_real_approved': reverse('mturk_manager:api_assignments_real_approved_tmp', args=[placeholder_slug_project]),
        # 'url_api_qualifications': reverse('mturk_manager:qualifications_for_project', args=[placeholder_slug_project]),
        # # 'url_api_qualification': reverse('mturk_manager:qualification_for_project', args=[placeholder_slug_project, 'da']),
        # 'url_api_global_db': reverse('mturk_manager:workers_for_project_global_db', args=[placeholder_slug_project]),
        
        'url_api_projects': Manager_Global_DB.get_url_absolute('projects'),
        'url_api_projects_check_uniqueness': Manager_Global_DB.get_url_absolute('info_projects/uniqueness'),
        'url_api_projects_settings_batch': Manager_Global_DB.get_url_absolute('projects/{}/settings_batch'.format(placeholder_slug_project)),
        'url_api_projects_templates_worker': Manager_Global_DB.get_url_absolute('projects/{}/templates_worker'.format(placeholder_slug_project)),
        'url_api_projects_batches': Manager_Global_DB.get_url_absolute('projects/{}/batches'.format(placeholder_slug_project)),
        
        'url_api_workers': Manager_Global_DB.get_url_absolute('projects/{}/workers'.format(placeholder_slug_project)),
        'url_api_workers_get_blocks_hard': Manager_Global_DB.get_url_absolute('projects/{}/workers/blocks_hard'.format(placeholder_slug_project)),

        'url_api_keywords': Manager_Global_DB.get_url_absolute('api/keywords'.format(placeholder_slug_project)),

        # 'url_api_batches': reverse('mturk_manager:batches_for_project', args=[placeholder_slug_project]),
        
        # 'url_api_keywords': reverse('mturk_manager:keywords'),
        # # 'url_api_project': reverse('mturk_manager:project_api_tmp'),
    }

    context = {}
    context['json_config'] = json.dumps(dict_config)
        
    return render(request, 'mturk_manager/app.html', context)