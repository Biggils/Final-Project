from rest_framework.permissions import BasePermission, SAFE_METHODS


class ProjectPermission(BasePermission):
    """
    Project owners have full control.
    Project members have read-only access.
    """

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True

        if request.method in SAFE_METHODS:
            return obj.members.filter(id=request.user.id).exists()

        return False


class TaskPermission(BasePermission):
    """
    Project owners have full control.
    Project members can view tasks.
    """

    def has_object_permission(self, request, view, obj):
        if obj.project.owner == request.user:
            return True

        if request.method in SAFE_METHODS:
            return obj.project.members.filter(
                id=request.user.id
            ).exists()

        return False