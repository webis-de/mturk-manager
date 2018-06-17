from mturk_manager.models import m_Project

def add_database_object_project(some_function):

    def wrapper(*args, **kwargs):
        try:
            slug_project = kwargs['slug_project']
        except KeyError:
            database_object_project = None
        else:
            database_object_project = m_Project.objects.get(slug=slug_project)

        kwargs['database_object_project'] = database_object_project   

        return some_function(*args, **kwargs)

    return wrapper