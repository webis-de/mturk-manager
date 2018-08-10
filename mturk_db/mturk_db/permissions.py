from rest_framework import permissions

class IsWorker(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'OPTIONS':
            return True
        return request.user.username == 'worker'

class IsInstance(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.username == 'instance'

class AllowOptionsAuthentication(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if request.method == 'OPTIONS':
            return True
        return request.user and request.user.is_authenticated