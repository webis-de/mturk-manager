from api.helpers import raise_not_implemented_exception


class Interface_Manager_Items(object):
    @staticmethod
    def get_all(database_object_project, request, fields=None   ):
        raise_not_implemented_exception('get_all', __class__)

    @staticmethod
    def get(id_item):
        raise_not_implemented_exception('get', __class__)

    @staticmethod
    def create(data):
        raise_not_implemented_exception('create', __class__)

    @staticmethod
    def update(instance, data):
        raise_not_implemented_exception('update', __class__)

    @staticmethod
    def delete(id_item):
        raise_not_implemented_exception('delete', __class__)
