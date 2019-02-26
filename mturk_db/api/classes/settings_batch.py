from api.classes import Interface_Manager_Items
from api.models import Account_Mturk, Settings_Batch, Keyword
from mturk_db.settings import URL_MTURK_SANDBOX
import boto3, json
from django.utils.text import slugify
from django.conf import settings

class Manager_Settings_Batch(Interface_Manager_Items):
    @staticmethod
    def get_all(database_object_project, request, fields=None):
        queryset = Settings_Batch.objects.filter(
            project=database_object_project,
            batch=None,
        )

        sort_by = request.query_params.get('sort_by')
        if sort_by is not None:
            descending = request.query_params.get('descending', 'false') == 'true'
            queryset = queryset.order_by(
                ('-' if descending else '') + sort_by
            )

        if fields is not None:
            queryset = queryset.values(
                *fields
            )

        return queryset

    @staticmethod
    def get(id_item):
        item = Settings_Batch.objects.get(
            pk=id_item
        )

        return item

    @staticmethod
    def create(data):
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
            dictionary_qualifications['qualification_locale'] = json.dumps(data['qualification_locale'])
        except KeyError:
            pass

        dictionary_settings = {}
        try:
            dictionary_settings['count_assignments_max_per_worker'] = data['count_assignments_max_per_worker']
        except KeyError:
            pass

        settings_batch = Settings_Batch.objects.create(
            project=data['database_object_project'],
            name=data['name'],

            title=data['title'],
            description=data['description'],
            reward=data['reward'],
            count_assignments=data['count_assignments'],
            lifetime=data['lifetime'],
            duration=data['duration'],
            template_worker=data['template_worker'],
            block_workers=data['block_workers'],
            has_content_adult=data['has_content_adult'],
            **dictionary_settings,
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

    @staticmethod
    def update(instance, data):
        for key, value in data.items():
            if key == 'keywords':
                instance.keywords.clear()
                list_keywords = []
                for keyword in data['keywords']:
                    try:
                        id_keyword = keyword['id']
                    except KeyError:
                        keyword = Keyword.objects.get_or_create(text=keyword['text'])[0]
                        list_keywords.append(keyword)
                    else:
                        list_keywords.append(id_keyword)

                instance.keywords.add(*list_keywords)
            elif key == 'qualification_locale':
                setattr(instance, key, json.dumps(value))
                
            else:
                setattr(instance, key, value)

        instance.save()

        return instance

    @staticmethod
    def delete(id_item):
        Settings_Batch.objects.filter(id=id_item).delete()
