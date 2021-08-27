from rest_framework import permissions

class  UpdateOwnProfile (permissions.BasePermission):
    """Allow user to edit their own profile"""

    def has_object_permission(self, request, view, obj):
        """"Check user is trying to edit their own profile"""

        has_permission = False

        if (request.method in permissions.SAFE_METHODS):
            has_permission = True
        else:
            has_permission = (obj.id == request.user.id)
        
        return has_permission