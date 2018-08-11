from api.models import Worker, Worker_Block_Project
from api.classes.projects import Manager_Projects
from api.enums import STATUS_BLOCK
# from django.db.models import F, Value, Count, Q, Sum, IntegerField, ExpressionWrapper
# from mturk_manager.classes import Manager_Qualifications

class Manager_Workers(object):

    # @classmethod
    # def get_all(cls, database_object_project, use_sandbox=True):

    # #     list_qualifications = Manager_Qualifications.load_from_mturk(database_object_project, use_sandbox)
    # #     queryset_qualifications = Model_Qualification.objects.all()

    # #     dictionary_database = {qualification.id_mturk: qualification for qualification in queryset_qualifications}   
    # #     set_ids_mturk = {qualification['QualificationTypeId'] for qualification in list_qualifications}        
    # #     set_ids_database = set(dictionary_database)        

    # #     set_ids_in_database_but_not_in_mturk = set_ids_database.difference(set_ids_mturk)
    # #     # delete unnecessary qualifications in database

    #     queryset_workers = m_Worker.objects.filter(
    #         fk_project=database_object_project
    #     ).annotate(
    #         count_assignments=Count('assignments', filter=Q(assignments__fk_hit__fk_batch__use_sandbox=use_sandbox))
    #     ).filter(
    #         count_assignments__gt=0
    #     )


    #     print([worker.count_assignments for worker in queryset_workers])
    #     return queryset_workers
    #     for qualification in list_qualifications:
    #         try:
    #             database_object_qualification = dictionary_database[qualification['QualificationTypeId']]
    #         except KeyError:
    #             pass
    #         else:
    #             qualification['name_database'] = database_object_qualification.name
    #             qualification['description_database'] = database_object_qualification.description

    #     return list_qualifications

    # @classmethod
    # def update(cls, database_object_project, name, validated_data, use_sandbox=True):
    #     print(validated_data)
    #     object_worker = m_Worker.objects.get(name=name, fk_project=database_object_project)
    #     for key, value in validated_data.items():
    #         print(key)
    #         if key == 'is_blocked':
    #             cls.update_status_block(
    #                 value_new=value['status_block_new'], 
    #                 value_old=value['status_block_old'], 
    #                 object_worker=object_worker, 
    #                 database_object_project=database_object_project, 
    #                 use_sandbox=use_sandbox
    #             )
    #         elif hasattr(object_worker, key):
    #             setattr(object_worker, key, value)

    #     # object_worker.is_blocked = validated_data.get('is_blocked')
    #     object_worker.save()
    #     return object_worker

    # @classmethod
    # def update_status_block(cls, value_new, value_old, object_worker, database_object_project, use_sandbox):
    #     print(value_new)
    #     print(value_old)
    #     print('######')
    #     # return
    #     client = Manager_Projects.get_mturk_api(database_object_project, use_sandbox)

    #     if value_old == STATUS_BLOCK.HARD:
            
    #         response = client.delete_worker_block(
    #             WorkerId=object_worker.name,
    #             Reason='unknown',
    #         )

    #     if value_new == STATUS_BLOCK.HARD:

    #         response = client.create_worker_block(
    #             WorkerId=object_worker.name,
    #             Reason='unknown',
    #         )

    #     if value_old == STATUS_BLOCK.SOFT:
    #         # raise Exception('Kristof forgot to remove this safety guard...')
    #         # response = client.disassociate_qualification_from_worker(
    #         #     QualificationTypeId=Manager_Qualifications.get_id_qualification_block_soft(database_object_project, use_sandbox),
    #         #     WorkerId=object_worker.name,
    #         #     SendNotification=False,
    #         # )
    #         response = client.associate_qualification_with_worker(
    #             QualificationTypeId=Manager_Qualifications.get_id_qualification_block_soft(database_object_project, use_sandbox),
    #             WorkerId=object_worker.name,
    #             IntegerValue=0,
    #             SendNotification=False,
    #         )

    #     if value_new == STATUS_BLOCK.SOFT:
    #         response = client.associate_qualification_with_worker(
    #             QualificationTypeId=Manager_Qualifications.get_id_qualification_block_soft(database_object_project, use_sandbox),
    #             WorkerId=object_worker.name,
    #             IntegerValue=1,
    #             SendNotification=False,
    #         )

    @classmethod
    def get_workers_blocked_hard(cls, use_sandbox):
        client = Manager_Projects.get_mturk_api(use_sandbox)

        paginator = client.get_paginator('list_worker_blocks')

        response_iterator = paginator.paginate(
            PaginationConfig={
                'PageSize': 100,
            }
        )

        set_workers_blocked_hard = set()

        for iterator in response_iterator:
            for block in iterator['WorkerBlocks']:
                set_workers_blocked_hard.add(block['WorkerId'])

        return set_workers_blocked_hard

    @classmethod
    def get_workers_blocked_soft(cls, database_object_project, use_sandbox):
        list_ids_workers = Worker_Block_Project.objects.filter(
            fk_project=database_object_project, is_sandbox=use_sandbox
        ).values_list('fk_worker__id_worker', flat=True)

        return set(list_ids_workers)

    @classmethod
    def get_status_block(cls, database_object_project, use_sandbox):
        set_workers_blocked_hard = cls.get_workers_blocked_hard(use_sandbox)
        set_workers_blocked_soft = cls.get_workers_blocked_soft(database_object_project, use_sandbox)

        return {
            'soft': set_workers_blocked_soft,
            'hard': set_workers_blocked_hard,
        }

    @classmethod
    def add_block_soft_for_worker(cls, id_worker, database_object_project, use_sandbox):
        object_worker = Worker.objects.get_or_create(id_worker=id_worker)[0]

        object_worker_block_project = Worker_Block_Project.objects.get_or_create(
            is_sandbox=use_sandbox,
            fk_project=database_object_project,
            fk_worker=object_worker,
        )[0]

    @classmethod
    def remove_block_soft_for_worker(cls, id_worker, database_object_project, use_sandbox):
        try:
            object_worker = Worker.objects.get_or_create(id_worker=id_worker)[0]
            object_worker_block_project = Worker_Block_Project.objects.filter(
                is_sandbox=use_sandbox,
                fk_project=database_object_project,
                fk_worker=object_worker,
            ).delete()
        except:
            pass

    @classmethod
    def get_status_block_for_worker(cls, database_object_project, id_worker):
        return {
            'is_blocked': Worker_Block_Project.objects.filter(
                fk_project=database_object_project,
                fk_worker__id_worker=id_worker,
            ).exists()
        }

    # @classmethod
    # def get_status_block(cls, database_object_project, use_sandbox):
    #     client = Manager_Projects.get_mturk_api(database_object_project, use_sandbox)

    #     id_qualification_block_soft = Manager_Qualifications.get_id_qualification_block_soft(database_object_project, use_sandbox)
    #     list_qualifications = Manager_Qualifications.get_workers_for_qualification(id_qualification_block_soft, database_object_project, use_sandbox)
    #     list_id_workers_blocked_soft = [qualification['WorkerId'] for qualification in list_qualifications if qualification['IntegerValue'] == 1]

    #     list_id_workers_blocked_hard = cls.get_workers_blocked(database_object_project, use_sandbox)



    #     # list_qualification_types = Manager_Qualifications.get_all_own_qualifications(database_object_project, use_sandbox)
    #     # print('++++++++++')

    #     # name_qualification_block_soft_hashed = Manager_Qualifications.get_name_qualification_block_soft_hashed(database_object_project)
    #     # print(name_qualification_block_soft_hashed)
    #     # id_qualification_type = [qualification['QualificationTypeId'] for qualification in list_qualification_types if qualification['Name'] == name_qualification_block_soft_hashed][0]

    #     # print(list_qualifications)
    #     # print('++++++++++')
    #     # queryset_workers = cls.get_all(database_object_project, use_sandbox)
        
    #     return {
    #         'soft': list_id_workers_blocked_soft,
    #         'hard': list_id_workers_blocked_hard,
    #     }