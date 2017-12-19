from mturk_manager.models import *
from mturk_manager.views.foo import test

test.test()

def glob_create_batch(db_obj_project, name):
    m_Batch.objects.get_or_create(name=name, defaults={
        'fk_project': db_obj_project
    })