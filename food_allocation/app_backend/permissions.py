from rest_framework.permissions import BasePermission


class IsNGOManager(BasePermission):
    """
    Custom permission to only allow access to users with is_ngo_manager flag.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_ngo_manager
