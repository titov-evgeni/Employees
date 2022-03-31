from rest_framework.permissions import BasePermission


class IsGroupEmployeeOnly(BasePermission):
    """The request is authenticated as employee from access group only"""

    ACCESS_GROUP = 'API Access'

    def has_permission(self, request, view):
        return request.user.groups.filter(name=self.ACCESS_GROUP)
