from mturk_manager.models import Global_DB
# from mturk_manager.classes.projects import Manager_Projects
# from mturk_manager.enums import STATUS_BLOCK
# from django.db.models import F, Value, Count, Q, Sum, IntegerField, ExpressionWrapper
# from mturk_manager.classes import Manager_Qualifications
from mturk.settings import URL_GLOBAL_DB
import requests, urllib

class Manager_Global_DB(object):
    try:
        object_global_db = Global_DB.objects.get(name='webis')
        headers = {
            'Authorization': 'Token {}'.format(object_global_db.token_instance)
        }
    except:
        print('No credentials for the global DB are set')


    @classmethod
    def get_url_absolute(cls, path='', use_sandbox=True):
        url = ''
        if path.startswith('/'):
            url = URL_GLOBAL_DB + path
        else:
            url = URL_GLOBAL_DB + '/' + path

        if not use_sandbox:
            url += '?use_sandbox=false'

        return url

    @classmethod
    def get_data(cls, database_object_project, use_sandbox):
        url = Manager_Global_DB.get_url_absolute('projects/{}/workers'.format(database_object_project.slug), use_sandbox)

        return requests.get(url, headers=cls.headers).json()

    @classmethod
    def add_block_soft_for_worker(cls, id_worker, database_object_project, use_sandbox):
        url = Manager_Global_DB.get_url_absolute('projects/{}/workers/{}/add_block_soft'.format(
            database_object_project.slug,
            id_worker,
        ), use_sandbox)

        return requests.post(url, headers=cls.headers)

    @classmethod
    def remove_block_soft_for_worker(cls, id_worker, database_object_project, use_sandbox):
        url = Manager_Global_DB.get_url_absolute('projects/{}/workers/{}/remove_block_soft'.format(
            database_object_project.slug,
            id_worker,
        ), use_sandbox)
        
        return requests.delete(url, headers=cls.headers)

    @classmethod
    def get_count_assignments_max_per_worker(cls, slug_project):
        url = Manager_Global_DB.get_url_absolute('projects/{}/count_assignments_max_per_worker'.format(
            slug_project
        ))
        
        return requests.get(url, headers=cls.headers).json()['count_assignments_max_per_worker']

    @classmethod
    def set_count_assignments_max_per_worker(cls, slug_project, value):
        url = Manager_Global_DB.get_url_absolute('projects/{}/count_assignments_max_per_worker/{}'.format(
            slug_project,
            value
        ))

        return requests.put(url, headers=cls.headers).json()['count_assignments_max_per_worker']

    @classmethod
    def update_count_assignments(cls, id_worker, value, database_object_project, use_sandbox):
        url = Manager_Global_DB.get_url_absolute('projects/{}/workers/{}/count_assignments'.format(
            database_object_project.slug,
            id_worker,
        ))

        return requests.put(url, data={'count': value}, headers=cls.headers).json()['count']
