from mturk_manager.models import Model_Qualification
from mturk_manager.classes.projects import Manager_Projects

class Manager_Qualifications(object):
    def __init__(self, arg):
        pass
        # super(Qualification, self).__init__()
        # self.arg = arg
        
    @staticmethod
    def get_all(database_object_project, use_sandbox=True):
        dictionary_qualifications = Manager_Qualifications.load_from_mturk(database_object_project, use_sandbox)
        queryset_qualifications = Model_Qualification.objects.all()

        dictionary_database = {qualification.id_mturk: qualification for qualification in queryset_qualifications}   
        set_ids_mturk = {qualification['QualificationTypeId'] for qualification in dictionary_qualifications}        
        set_ids_database = set(dictionary_database)        

        set_ids_in_database_but_not_in_mturk = set_ids_database.difference(set_ids_mturk)
        # delete unnecessary qualifications in database
        Model_Qualification.objects.filter(id_mturk__in=set_ids_in_database_but_not_in_mturk).delete()

        for qualification in dictionary_qualifications:
            id_mturk_qualification = qualification['QualificationTypeId']
            # print(qualification.keys())
            try:
                database_object_qualification = dictionary_database[dictionary_database[id_mturk_qualification]]
            except KeyError:
                pass
            else:
                qualification['name_database'] = database_object_qualification.name
                qualification['description_database'] = database_object_qualification.description


        return dictionary_qualifications

    @staticmethod
    def load_from_mturk(database_object_project, use_sandbox=True):
        client = Manager_Projects.get_mturk_api(database_object_project, use_sandbox)

        response = client.list_qualification_types(
            MustBeRequestable=False,
            MustBeOwnedByCaller=True,
        )

        return response['QualificationTypes']
