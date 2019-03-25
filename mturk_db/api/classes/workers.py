import json

from api.classes import Interface_Manager_Items
from api.models import Worker, Worker_Block_Project, Count_Assignments_Worker_Project, Assignment_Worker
from api.classes.projects import Manager_Projects
from api.enums import STATUS_BLOCK
import botocore
from django.db.models import F, Q, When, Case, BooleanField, IntegerField, Count, Value, Subquery, OuterRef
from django.db.models.functions import Coalesce
# from django.db.models import F, Value, Count, Q, Sum, IntegerField, ExpressionWrapper
# from mturk_manager.classes import Manager_Qualifications

class Manager_Workers(Interface_Manager_Items):
    # @classmethod
    # def sync_workers_by_ids(cls, database_object_project, data, use_sandbox=True):
    #     foo = Count_Assignments_Worker_Project.objects.filter(
    #         worker=OuterRef('pk'),
    #         # project=database_object_project,
    #     )
    #
    #     return Worker.objects.filter(
    #         id__in=data
    #     ).annotate(
    #         count_worker_blocks=Coalesce(Count('worker_blocks_project', filter=Q(worker_blocks_project__project=database_object_project)), 0)
    #     ).annotate(
    #         is_blocked_soft=Case(
    #             When(count_worker_blocks=1, then=Value(True)),
    #             default=Value(False),
    #             output_field=BooleanField(),
    #         ),
    #         count_assignments_limit=Subquery(foo.filter(project=database_object_project).values('count_assignments')[:1]),
    #         # count_assignments_limit=Q('count_assignments__count_assignments'),
    #         # count_assignments_limit=Case(
    #         #     When(count_assignments__project=database_object_project, then=Value(1)),
    #         #     default=Value(None),
    #         #     output_field=IntegerField(),
    #         # )
    #     )

    @staticmethod
    def get(id_item):
        item = Worker.objects.get(
            pk=id_item
        )

        return item

    @staticmethod
    def get_all(database_object_project, request, fields=None, use_sandbox=True):
        foo = Count_Assignments_Worker_Project.objects.filter(
            worker=OuterRef('pk'),
            # project=database_object_project,
        )

        queryset = Worker.objects.filter(
            assignments__hit__batch__project=database_object_project,
            assignments__hit__batch__use_sandbox=use_sandbox,
        ).distinct()

        workers_selected = request.query_params.getlist('workersSelected[]')
        if len(workers_selected) > 0:
            queryset = queryset.filter(id_worker__in=workers_selected)

        states_block = set(request.query_params.getlist('statesBlock[]'))
        combine_with_and = json.loads(request.query_params.get('combineWithAnd', 'false'))
        # if len(states_block) > 0:
        if combine_with_and == True:
            print('COMBINE WITH AND')
            block_soft = 'block_soft' in states_block
            queryset = queryset.filter(is_blocked_global=block_soft)

            block_project = 'block_project' in states_block
            if block_project == True:
                queryset = queryset.filter(worker_blocks_project__project=database_object_project)
            else:
                queryset = queryset.exclude(worker_blocks_project__project=database_object_project)
        else:
            pass

        queryset = queryset.annotate(
            count_worker_blocks=Coalesce(
                Count(
                    'worker_blocks_project',
                    filter=Q(worker_blocks_project__project=database_object_project),
                    distinct=True
                ),
                0
            )
        ).annotate(
            is_blocked_soft=Case(
                When(count_worker_blocks=1, then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            ),
            count_assignments_limit=Subquery(
                foo.filter(project=database_object_project).values('count_assignments')[:1]),
            # count_assignments_limit=Q('count_assignments__count_assignments'),
            # count_assignments_limit=Case(
            #     When(count_assignments__project=database_object_project, then=Value(1)),
            #     default=Value(None),
            #     output_field=IntegerField(),
            # )

        )

        show_workers_blocked_none = json.loads(request.query_params.get('show_workers_blocked_none', 'true'))
        # if show_workers_blocked_none == False:
        #     queryset = queryset.exclude(count_assignments_limit=True)

        show_workers_blocked_limit = json.loads(request.query_params.get('show_workers_blocked_limit', 'true'))
        if show_workers_blocked_limit == False:
            queryset = queryset.exclude(count_assignments_limit__gt=database_object_project.count_assignments_max_per_worker)

        show_workers_blocked_soft = json.loads(request.query_params.get('show_workers_blocked_soft', 'true'))
        if show_workers_blocked_soft == False:
            queryset = queryset.exclude(is_blocked_soft=True)

        if fields is not None:
            queryset = queryset.values(
                *fields
            )

        return queryset

    @staticmethod
    def update(instance, data):
        for key, value in data.items():
            print(key)
            if key == 'is_blocked_soft':
                instance.is_blocked_soft = Manager_Workers.update_status_block_soft(
                    is_blocked=value, 
                    instance=instance, 
                    database_object_project=data['database_object_project'],
                    use_sandbox=data['use_sandbox'],
                )
            elif key == 'is_blocked_hard':
                instance.is_blocked_hard = Manager_Workers.update_status_block_hard(
                    is_blocked=value, 
                    instance=instance, 
                    database_object_project=data['database_object_project'],
                    use_sandbox=data['use_sandbox'],
                )
            elif key == 'count_assignments_limit':
                instance.count_assignments_limit = Manager_Workers.update_count_assignments(
                    count_assignments_limit=value, 
                    instance=instance, 
                    database_object_project=data['database_object_project'],
                    use_sandbox=data['use_sandbox'],
                )
            elif hasattr(instance, key):
                setattr(instance, key, value)

        # instance.is_blocked = validated_data.get('is_blocked')
        instance.save()
        return instance

    @classmethod
    def update_count_assignments(cls, count_assignments_limit, instance, database_object_project, use_sandbox):
        count_assignments_worker_project, was_created = Count_Assignments_Worker_Project.objects.get_or_create(
            project=database_object_project,
            worker=instance,
            defaults={
                'count_assignments': count_assignments_limit, 
            }
        )

        if not was_created:
            count_assignments_worker_project.count_assignments = count_assignments_limit
            count_assignments_worker_project.save()
        
        return count_assignments_limit

    @classmethod
    def update_status_block_hard(cls, is_blocked, instance, database_object_project, use_sandbox):
        client = Manager_Projects.get_mturk_api(use_sandbox)

        if is_blocked:
            response = client.create_worker_block(
                WorkerId=instance.id_worker,
                Reason='unknown',
            )
        else:
            response = client.delete_worker_block(
                WorkerId=instance.id_worker,
                Reason='unknown',
            )
        return is_blocked
    
    @classmethod
    def get_blocks_hard(cls, database_object_project, data, use_sandbox):
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
                set_workers_blocked_hard.add(block['WorkerId'].upper())

        return Worker.objects.filter(id_worker__in=set_workers_blocked_hard).values_list('id', flat=True)


    @classmethod
    def update_status_block_soft(cls, is_blocked, instance, database_object_project, use_sandbox):
        if is_blocked:
            cls.add_block_soft_for_worker(instance, database_object_project, use_sandbox)
        else:
            cls.remove_block_soft_for_worker(instance, database_object_project, use_sandbox)

        return is_blocked

    @classmethod
    def add_block_soft_for_worker(cls, instance, database_object_project, use_sandbox):
        # object_worker = Worker.objects.get_or_create(id_worker=id_worker)[0]

        object_worker_block_project = Worker_Block_Project.objects.get_or_create(
            # is_sandbox=use_sandbox,
            project=database_object_project,
            worker=instance,
        )[0]

    @classmethod
    def remove_block_soft_for_worker(cls, instance, database_object_project, use_sandbox):
        try:
            # object_worker = Worker.objects.get_or_create(id_worker=id_worker)[0]
            object_worker_block_project = Worker_Block_Project.objects.filter(
                # is_sandbox=use_sandbox,
                project=database_object_project,
                worker=instance,
            ).delete()
        except:
            pass
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
        try:
            set_workers_blocked_hard = cls.get_workers_blocked_hard(use_sandbox)
        except botocore.exceptions.EndpointConnectionError:
            set_workers_blocked_hard = None

        set_workers_blocked_soft = cls.get_workers_blocked_soft(database_object_project, use_sandbox)

        return {
            'soft': set_workers_blocked_soft,
            'hard': set_workers_blocked_hard,
        }

    @classmethod
    def get_status_block_for_worker(cls, database_object_project, id_worker):
        id_worker = id_worker.upper()
        is_blocked = False

        # check if project block is active
        if Worker_Block_Project.objects.filter(
                project=database_object_project,
                worker__id_worker=id_worker,
            ).exists():
            is_blocked = True
        else:
            try:
                worker = Worker.objects.get(id_worker=id_worker)
            except Worker.DoesNotExist:
                worker = None

            if worker != None and worker.is_blocked_global:
                is_blocked = True
            else:
                # if a limit for this batch is set
                if database_object_project.count_assignments_max_per_worker != None:

                    queryset = Count_Assignments_Worker_Project.objects.filter(
                        project=database_object_project,
                        worker__id_worker=id_worker,
                    )

                    count_assignments = 0

                    if len(queryset) == 1:
                        count_assignments = queryset[0].count_assignments

                    # is never true if limit of worker is -1
                    is_blocked = count_assignments >= database_object_project.count_assignments_max_per_worker

        return {
            # 'is_blocked': True,
            'is_blocked': is_blocked,
        }

        # return {
        #     'is_blocked': Worker_Block_Project.objects.filter(
        #         fk_project=database_object_project,
        #         fk_worker__id_worker=id_worker,
        #     ).exists()
        # }


    @classmethod
    def get_counters(cls, database_object_project, use_sandbox):
        queryset = Count_Assignments_Worker_Project.objects.filter(
            fk_project=database_object_project,
        ).select_related('fk_worker')

        return {count_assignments_worker_project.fk_worker.id_worker:count_assignments_worker_project.count_assignments for count_assignments_worker_project in queryset}

    @classmethod
    def get_counter(cls, database_object_project, use_sandbox):
        dictionary_counters = cls.get_counters(database_object_project, use_sandbox)

        return dictionary_counters

    @classmethod
    def increment_counter_for_worker(cls, database_object_project, data):
        id_worker = data['id_worker'].upper()
        id_assignment = data['id_assignment'].upper()

        assignment_worker, was_created_assignment_worker = Assignment_Worker.objects.get_or_create(
            id_worker=id_worker,
            id_assignment=id_assignment,
        )

        # only if first request for this assignment
        if was_created_assignment_worker:
            worker = Worker.objects.get_or_create(id_worker=id_worker)[0]

            count_assignments_worker_project, was_created = Count_Assignments_Worker_Project.objects.get_or_create(
                project=database_object_project,
                worker=worker,
                defaults={
                    'count_assignments': 1, 
                }
            )

            if not was_created:
                if count_assignments_worker_project.count_assignments > -1:
                    count_assignments_worker_project.count_assignments += 1
                    count_assignments_worker_project.save()

        return {
            'incremented': was_created_assignment_worker,
        }

    @classmethod
    def set_count_assignments(cls, database_object_project, id_worker, value):
        id_worker = id_worker.upper()
        worker = Worker.objects.get_or_create(id_worker=id_worker)[0]

        count_rows = Count_Assignments_Worker_Project.objects.filter(
            project=database_object_project,
            worker=worker,
        ).update(count_assignments=value)

        if count_rows == 0:
            Count_Assignments_Worker_Project.objects.create(
                project=database_object_project,
                worker=worker,
                count_assignments=value, 
            )

        Assignment_Worker.objects.filter(id_worker=id_worker).delete()

        return {'count': value}
        # print(database_object_project)
        # print(id_worker)
        # print(value)

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