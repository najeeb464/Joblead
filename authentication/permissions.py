from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return getattr(request.user, "role", None) == 'Admin'


class IsAdminOrSalesAgent(permissions.BasePermission):
 
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return getattr(request.user, "role", None) in ['Admin', 'SalesAgent']


class IsAssignedTechnician(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if getattr(request.user, "role", None) == 'Admin':
            return True
        return getattr(obj.job, "assigned_to", None) == request.user
