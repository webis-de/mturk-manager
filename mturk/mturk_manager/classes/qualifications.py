from mturk_manager.models import Model_Qualification
from mturk_manager.classes.projects import Manager_Projects
from secrets import token_urlsafe

class Manager_Qualifications(object):
    def __init__(self, arg):
        pass
        # super(Qualification, self).__init__()
        # self.arg = arg
        
    @staticmethod
    def get_all(database_object_project, use_sandbox=True):
        list_qualifications = Manager_Qualifications.load_from_mturk(database_object_project, use_sandbox)
        queryset_qualifications = Model_Qualification.objects.all()

        dictionary_database = {qualification.id_mturk: qualification for qualification in queryset_qualifications}   
        set_ids_mturk = {qualification['QualificationTypeId'] for qualification in list_qualifications}        
        set_ids_database = set(dictionary_database)        

        set_ids_in_database_but_not_in_mturk = set_ids_database.difference(set_ids_mturk)
        # delete unnecessary qualifications in database
        Model_Qualification.objects.filter(id_mturk__in=set_ids_in_database_but_not_in_mturk).delete()
        for qualification in list_qualifications:
            try:
                database_object_qualification = dictionary_database[qualification['QualificationTypeId']]
            except KeyError:
                pass
            else:
                qualification['name_database'] = database_object_qualification.name
                qualification['description_database'] = database_object_qualification.description

        return list_qualifications

    @staticmethod
    def delete(database_object_project, list_ids, use_sandbox=True):
        client = Manager_Projects.get_mturk_api(database_object_project, use_sandbox)
        print(list_ids)
        count_deleted = 0
        for id_mturk in list_ids:
            response = client.delete_qualification_type(
                QualificationTypeId=id_mturk
            )
            print(response)
            count_deleted += 1

        Model_Qualification.objects.filter(id_mturk__in=list_ids).delete()
        
        return count_deleted

    @staticmethod
    def create(database_object_project, validated_data, use_sandbox=True):
        client = Manager_Projects.get_mturk_api(database_object_project, use_sandbox)

        name_mturk = validated_data.get('Name')
        if name_mturk == None:
            name_mturk = token_urlsafe()
        description_mturk = validated_data.get('Description')
        if description_mturk == None:
            description_mturk = token_urlsafe()

        print(validated_data)
        response = client.create_qualification_type(
            Name=name_mturk,
            Keywords=validated_data.get('Keywords', ''),
            Description=description_mturk,
            QualificationTypeStatus=validated_data.get('QualificationTypeStatus', 'Inactive'),
            # QualificationTypeStatus='Active' if validated_data.get('is_active') else 'Inactive',
            # Name=validated_data.get('name_database'),
        )['QualificationType']

        print(response)

        object_qualification = Model_Qualification.objects.create(
            id_mturk=response['QualificationTypeId'],
            name=validated_data.get('name_database'),
            description=validated_data.get('description_database'),
        )

        response['name_database'] = validated_data.get('name_database')
        response['description_database'] = validated_data.get('description_database')

        return response


    @staticmethod
    def update(database_object_project, id_mturk, validated_data, use_sandbox=True):
        print(validated_data)
        dictionary_changed_fields = {
            'QualificationTypeId': id_mturk,
        }

        description_mturk = validated_data.get('Description')
        if description_mturk != None:
            dictionary_changed_fields['Description'] = description_mturk

        # is_active = validated_data.get('QualificationTypeStatus', 'Inactive')
        # if is_active != None:
        #     dictionary_changed_fields['QualificationTypeStatus'] = is_active

            # Description=description_mturk,
            # QualificationTypeStatus=validated_data.get('QualificationTypeStatus', 'Inactive'),
        print(dictionary_changed_fields)

        if len(dictionary_changed_fields) > 1:
            client = Manager_Projects.get_mturk_api(database_object_project, use_sandbox)
            response = client.update_qualification_type(
                **dictionary_changed_fields
                # QualificationTypeStatus='Active' if validated_data.get('is_active') else 'Inactive',
                # Name=validated_data.get('name_database'),
            )['QualificationType']

        ###########################
        ###########################
        ###########################
        dictionary_changed_fields = {}

        name_database = validated_data.get('name_database')
        if name_database != None:
            dictionary_changed_fields['name'] = name_database

        description_database = validated_data.get('description_database')
        if description_database != None:
            dictionary_changed_fields['description'] = description_database

        was_created = False
        try:
            object_qualification = Model_Qualification.objects.get(id_mturk=id_mturk)
        except Model_Qualification.DoesNotExist:
            if len(dictionary_changed_fields) < 2:
                # if it does not exist and is not required
                return response
            else:
                was_created = True
                object_qualification = Model_Qualification.objects.create(
                    id_mturk=id_mturk,
                    **dictionary_changed_fields
                )

        if not was_created:
            object_qualification.name = validated_data.get('name_database')
            object_qualification.description = validated_data.get('description_database')
            object_qualification.save()

        response['name_database'] = object_qualification.name
        response['description_database'] = object_qualification.description

        return response


    @staticmethod
    def load_from_mturk(database_object_project, use_sandbox=True):
        client = Manager_Projects.get_mturk_api(database_object_project, use_sandbox)

        response = client.list_qualification_types(
            MustBeRequestable=False,
            MustBeOwnedByCaller=True,
        )

        return response['QualificationTypes']
