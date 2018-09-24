from api.models import Account_Mturk, Settings_Batch, Keyword
from mturk_db.settings import URL_MTURK_SANDBOX
import boto3
from django.utils.text import slugify
from django.conf import settings

class Manager_Settings_Batch(object):
    try:
        object_account_mturk = Account_Mturk.objects.get(name='webis')
    except:
        print('No credentials for the MTurk account are set')

    @classmethod
    def get_all_for_project(cls, id_project):
        return Settings_Batch.objects.filter(project=id_project)

    @classmethod
    def create(cls, data):
        dictionary_qualifications = {}
        try:
            dictionary_qualifications['qualification_assignments_approved'] = data['qualification_assignments_approved']
        except KeyError:
            pass
        try:
            dictionary_qualifications['qualification_hits_approved'] = data['qualification_hits_approved']
        except KeyError:
            pass
        try:
            dictionary_qualifications['qualification_locale'] = data['qualification_locale']
        except KeyError:
            pass

        settings_batch = Settings_Batch.objects.create(
            project = data['database_object_project'],
            name=data['name'],

            title=data['title'],
            description=data['description'],
            reward=data['reward'],
            count_assignments=data['count_assignments'],
            count_assignments_max_per_worker=data['count_assignments_max_per_worker'],
            lifetime=data['lifetime'],
            duration=data['duration'],
            template_worker=data['template_worker'],
            block_workers=data['block_workers'],
            has_content_adult=data['has_content_adult'],
            **dictionary_qualifications,
        )

        list_keywords = []
        for keyword in data['keywords']:
            try:
                id_keyword = keyword['id']
            except KeyError:
                keyword = Keyword.objects.get_or_create(text=keyword['text'])[0]
                list_keywords.append(keyword)
            else:
                list_keywords.append(id_keyword)

        print(list_keywords)
        settings_batch.keywords.add(*list_keywords)

        return settings_batch
