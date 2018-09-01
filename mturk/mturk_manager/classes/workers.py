from mturk_manager.models import m_Worker
from mturk_manager.classes.projects import Manager_Projects
from mturk_manager.classes.projects import Manager_Projects
from mturk_manager.enums import STATUS_BLOCK
from django.db.models import F, Value, Count, Q, Sum, IntegerField, ExpressionWrapper
from mturk_manager.classes import Manager_Qualifications
from mturk_manager.classes import Manager_Global_DB
import time

class Manager_Workers(object):
    @classmethod
    def get_all(cls, database_object_project, use_sandbox=True):

    #     list_qualifications = Manager_Qualifications.load_from_mturk(database_object_project, use_sandbox)
    #     queryset_qualifications = Model_Qualification.objects.all()

    #     dictionary_database = {qualification.id_mturk: qualification for qualification in queryset_qualifications}   
    #     set_ids_mturk = {qualification['QualificationTypeId'] for qualification in list_qualifications}        
    #     set_ids_database = set(dictionary_database)        

    #     set_ids_in_database_but_not_in_mturk = set_ids_database.difference(set_ids_mturk)
    #     # delete unnecessary qualifications in database

        queryset_workers = m_Worker.objects.filter(
            fk_project=database_object_project
        ).annotate(
            count_assignments=Count('assignments', filter=Q(assignments__fk_hit__fk_batch__use_sandbox=use_sandbox))
        ).filter(
            count_assignments__gt=0
        )


        print([worker.count_assignments for worker in queryset_workers])
        return queryset_workers
    #     for qualification in list_qualifications:
    #         try:
    #             database_object_qualification = dictionary_database[qualification['QualificationTypeId']]
    #         except KeyError:
    #             pass
    #         else:
    #             qualification['name_database'] = database_object_qualification.name
    #             qualification['description_database'] = database_object_qualification.description

    #     return list_qualifications

    @classmethod
    def update(cls, database_object_project, name, validated_data, use_sandbox=True):
        print(validated_data)
        object_worker = m_Worker.objects.get(name=name, fk_project=database_object_project)
        for key, value in validated_data.items():
            print(key)
            if key == 'is_blocked_soft':
                object_worker.is_blocked_soft = cls.update_status_block_soft(
                    is_blocked=value, 
                    object_worker=object_worker, 
                    database_object_project=database_object_project, 
                    use_sandbox=use_sandbox
                )
            elif key == 'is_blocked_hard':
                object_worker.is_blocked_hard = cls.update_status_block_hard(
                    is_blocked=value, 
                    object_worker=object_worker, 
                    database_object_project=database_object_project, 
                    use_sandbox=use_sandbox
                )
            elif key == 'counter_assignments':
                object_worker.counter_assignments = cls.update_count_assignments(
                    value=value, 
                    object_worker=object_worker, 
                    database_object_project=database_object_project, 
                    use_sandbox=use_sandbox
                )
            elif hasattr(object_worker, key):
                setattr(object_worker, key, value)

        # object_worker.is_blocked = validated_data.get('is_blocked')
        object_worker.save()
        return object_worker

    @classmethod
    def update_count_assignments(cls, value, object_worker, database_object_project, use_sandbox):
        return Manager_Global_DB.update_count_assignments(object_worker.name, value, database_object_project, use_sandbox)


    @classmethod
    def update_status_block_hard(cls, is_blocked, object_worker, database_object_project, use_sandbox):
        client = Manager_Projects.get_mturk_api(database_object_project, use_sandbox)

        if is_blocked:
            response = client.create_worker_block(
                WorkerId=object_worker.name,
                Reason='unknown',
            )
        else:
            response = client.delete_worker_block(
                WorkerId=object_worker.name,
                Reason='unknown',
            )
        return is_blocked

    @classmethod
    def update_status_block_soft(cls, is_blocked, object_worker, database_object_project, use_sandbox):
        if is_blocked:
            Manager_Global_DB.add_block_soft_for_worker(object_worker.name, database_object_project, use_sandbox)
        else:
            Manager_Global_DB.remove_block_soft_for_worker(object_worker.name, database_object_project, use_sandbox)

        return is_blocked

    @classmethod
    def get_workers_blocked(cls, database_object_project, use_sandbox):
        client = Manager_Projects.get_mturk_api(database_object_project, use_sandbox)

        paginator = client.get_paginator('list_worker_blocks')

        response_iterator = paginator.paginate(
            PaginationConfig={
                'PageSize': 100,
            }
        )

        list_workers = []

        for iterator in response_iterator:
            for block in iterator['WorkerBlocks']:
                list_workers.append(block['WorkerId'])

        return list_workers

    @classmethod
    def get_data_global_db(cls, database_object_project, use_sandbox):
        return Manager_Global_DB.get_data(database_object_project, use_sandbox)