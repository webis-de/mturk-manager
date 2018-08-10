from api.models import Project
from urllib.parse import parse_qs

def add_database_object_project(some_function):

    def wrapper(*args, **kwargs):
        try:
            slug_project = kwargs['slug_project']
        except KeyError:
            database_object_project = None
        else:
            database_object_project = Project.objects.get_or_create(slug=slug_project)[0]

        kwargs['database_object_project'] = database_object_project 
        # print(args)
        # print(args)
        # print(kwargs)
        # print(parse_qs(args[1]))
        # print(parse_qs(args[1].META))
        # print(parse_qs(args[1].META))

        try:
            request = args[1]
        except IndexError:
            request = args[0]

        # print(request)
        try:
            use_sandbox = False if parse_qs(request.META['QUERY_STRING'])['use_sandbox'][0] == 'false' else True
        except KeyError:
            use_sandbox = True

        kwargs['use_sandbox'] = use_sandbox 

        return some_function(*args, **kwargs)

    return wrapper