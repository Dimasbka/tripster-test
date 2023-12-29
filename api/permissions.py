from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """ права что бы редактировать и удалять свои оценки """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user