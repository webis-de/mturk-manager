from mturk_manager.models import m_Worker
from mturk_manager.classes.projects import Manager_Projects
from mturk_manager.enums import STATUS_BLOCK
from django.db.models import F, Value, Count, Q, Sum, IntegerField, ExpressionWrapper

class Manager_Workers(object):
    def __init__(self, arg):
        pass
        # super(Qualification, self).__init__()
        # self.arg = arg
        
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
        object_worker = m_Worker.objects.get(name=name, fk_project=database_object_project)
        for key, value in validated_data.items():
            if hasattr(object_worker, key):
                if key == 'is_blocked':
                    cls.update_status_block(
                        value_new=value, 
                        value_old=object_worker.is_blocked, 
                        object_worker=object_worker, 
                        database_object_project=database_object_project, 
                        use_sandbox=use_sandbox
                    )

                setattr(object_worker, key, value)

        # object_worker.is_blocked = validated_data.get('is_blocked')
        object_worker.save()
        return object_worker

    @classmethod
    def update_status_block(cls, value_new, value_old, object_worker, database_object_project, use_sandbox):
        # print(value_new)
        # print(value_old)
        if value_old == STATUS_BLOCK.HARD and value_new != STATUS_BLOCK.HARD:
            client = Manager_Projects.get_mturk_api(database_object_project, use_sandbox)
            
            response = client.delete_worker_block(
                WorkerId=object_worker.name,
                Reason='unknown',
            )

        elif value_new == STATUS_BLOCK.HARD:
            client = Manager_Projects.get_mturk_api(database_object_project, use_sandbox)

            response = client.create_worker_block(
                WorkerId=object_worker.name,
                Reason='unknown',
            )
            

        #     print('HARD')
        # else:


        # print(response)
        # return response['QualificationTypes']