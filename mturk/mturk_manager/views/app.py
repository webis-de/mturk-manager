from django.shortcuts import render, redirect
from django.urls import reverse
import json
# from mturk_manager.models import *
# import urllib.parse
# from mturk_manager.views import code_shared
from django.middleware.csrf import get_token
# from mturk_manager.classes import Manager_Global_DB
from django.conf import settings as settings_django

def app(request):
    placeholder_slug_project = 'PLACEHOLDER_SLUG_PROJECT'
    if settings_django.URL_GLOBAL_DB == None:
        dict_config = {}
    else:
        dict_config = {
            'token_instance': settings_django.TOKEN_INSTANCE,
            'token_csrf': get_token(request),
            # 'url_project': reverse('mturk_manager:project', args=[placeholder_slug_project]),
            # 'url_api_get_balance': reverse('mturk_manager:balance', args=[placeholder_slug_project]),
            # 'url_api_assignments_real_approved': reverse('mturk_manager:api_assignments_real_approved_tmp', args=[placeholder_slug_project]),
            # 'url_api_qualifications': reverse('mturk_manager:qualifications_for_project', args=[placeholder_slug_project]),
            # # 'url_api_qualification': reverse('mturk_manager:qualification_for_project', args=[placeholder_slug_project, 'da']),
            # 'url_api_global_db': reverse('mturk_manager:workers_for_project_global_db', args=[placeholder_slug_project]),
            
            'url_api_projects': get_url_absolute('projects'),
            'url_api_projects_check_uniqueness': get_url_absolute('info_projects/uniqueness'),
            'url_api_projects_settings_batch': get_url_absolute('projects/{}/settings_batch'.format(placeholder_slug_project)),
            'url_api_projects_templates_worker': get_url_absolute('projects/{}/templates_worker'.format(placeholder_slug_project)),
            'url_api_projects_templates_assignment': get_url_absolute('projects/{}/templates_assignment'.format(placeholder_slug_project)),
            'url_api_projects_templates_hit': get_url_absolute('projects/{}/templates_hit'.format(placeholder_slug_project)),
            'url_api_projects_templates_global': get_url_absolute('projects/{}/templates_global'.format(placeholder_slug_project)),
            'url_api_projects_batches': get_url_absolute('projects/{}/batches'.format(placeholder_slug_project)),
            'url_api_projects_batches_download': get_url_absolute('projects/{}/download_batches'.format(placeholder_slug_project)),
            'url_api_projects_batches_download_info': get_url_absolute('projects/{}/download_info_batches'.format(placeholder_slug_project)),
            'url_api_projects_hits': get_url_absolute('projects/{}/hits'.format(placeholder_slug_project)),
            'url_api_projects_assignments': get_url_absolute('projects/{}/assignments'.format(placeholder_slug_project)),
            'url_api_projects_clear_sandbox': get_url_absolute('projects/{}/clear_sandbox'.format(placeholder_slug_project)),
            'url_api_ping': get_url_absolute('projects/{}/ping'.format(placeholder_slug_project)),
            
            'url_api_workers': get_url_absolute('projects/{}/workers'.format(placeholder_slug_project)),
            'url_api_workers_get_blocks_hard': get_url_absolute('projects/{}/workers/blocks_hard'.format(placeholder_slug_project)),

            'url_api_keywords': get_url_absolute('api/keywords'.format(placeholder_slug_project)),
            'url_api_messages_reject': get_url_absolute('api/messages_reject'.format(placeholder_slug_project)),

            # 'url_api_batches': reverse('mturk_manager:batches_for_project', args=[placeholder_slug_project]),
            
            # 'url_api_keywords': reverse('mturk_manager:keywords'),
            # # 'url_api_project': reverse('mturk_manager:project_api_tmp'),
        }

    context = {}
    context['json_config'] = json.dumps(dict_config)
        
    return render(request, 'mturk_manager/app.html', context)


def get_url_absolute(path='', use_sandbox=True):
    url = ''
    if path.startswith('/'):
        url = settings_django.URL_GLOBAL_DB + path
    else:
        url = settings_django.URL_GLOBAL_DB + '/' + path

    if not use_sandbox:
        url += '?use_sandbox=false'

    return url