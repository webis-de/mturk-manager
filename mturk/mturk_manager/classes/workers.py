from mturk_manager.models import m_Worker
from mturk_manager.classes.projects import Manager_Projects
from mturk_manager.enums import STATUS_BLOCK
from django.db.models import F, Value, Count, Q, Sum, IntegerField, ExpressionWrapper
from mturk_manager.classes import Manager_Qualifications

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
            if key == 'is_blocked':
                cls.update_status_block(
                    value_new=value['status_block_new'], 
                    value_old=value['status_block_old'], 
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
    def update_status_block(cls, value_new, value_old, object_worker, database_object_project, use_sandbox):
        print(value_new)
        print(value_old)
        print('######')
        # return
        client = Manager_Projects.get_mturk_api(database_object_project, use_sandbox)

        if value_old == STATUS_BLOCK.HARD:
            
            response = client.delete_worker_block(
                WorkerId=object_worker.name,
                Reason='unknown',
            )

        if value_new == STATUS_BLOCK.HARD:

            response = client.create_worker_block(
                WorkerId=object_worker.name,
                Reason='unknown',
            )

        if value_old == STATUS_BLOCK.SOFT:
            # raise Exception('Kristof forgot to remove this safety guard...')
            # response = client.disassociate_qualification_from_worker(
            #     QualificationTypeId=Manager_Qualifications.get_id_qualification_block_soft(database_object_project, use_sandbox),
            #     WorkerId=object_worker.name,
            # )
            response = client.associate_qualification_with_worker(
                QualificationTypeId=Manager_Qualifications.get_id_qualification_block_soft(database_object_project, use_sandbox),
                WorkerId=object_worker.name,
                IntegerValue=0,
                SendNotification=False,
            )

        if value_new == STATUS_BLOCK.SOFT:
            response = client.associate_qualification_with_worker(
                QualificationTypeId=Manager_Qualifications.get_id_qualification_block_soft(database_object_project, use_sandbox),
                WorkerId=object_worker.name,
                IntegerValue=1,
                SendNotification=False,
            )

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
    def get_status_block(cls, database_object_project, use_sandbox):
        client = Manager_Projects.get_mturk_api(database_object_project, use_sandbox)

        id_qualification_block_soft = Manager_Qualifications.get_id_qualification_block_soft(database_object_project, use_sandbox)
        list_qualifications = Manager_Qualifications.get_workers_for_qualification(id_qualification_block_soft, database_object_project, use_sandbox)
        list_id_workers_blocked_soft = [qualification['WorkerId'] for qualification in list_qualifications if qualification['IntegerValue'] == 1]

        list_id_workers_blocked_hard = cls.get_workers_blocked(database_object_project, use_sandbox)



        # list_qualification_types = Manager_Qualifications.get_all_own_qualifications(database_object_project, use_sandbox)
        # print('++++++++++')

        # name_qualification_block_soft_hashed = Manager_Qualifications.get_name_qualification_block_soft_hashed(database_object_project)
        # print(name_qualification_block_soft_hashed)
        # id_qualification_type = [qualification['QualificationTypeId'] for qualification in list_qualification_types if qualification['Name'] == name_qualification_block_soft_hashed][0]

        # print(list_qualifications)
        # print('++++++++++')
        # queryset_workers = cls.get_all(database_object_project, use_sandbox)
        
        return {
            'soft': list_id_workers_blocked_soft,
            'hard': list_id_workers_blocked_hard,
        }