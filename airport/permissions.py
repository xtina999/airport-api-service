from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminALLORIsAuthenticatedReadOnly(BasePermission):
    """
    The request is authenticated as on admin user,
    or is a read-only for non-admin user request.
    """

    def has_permission(self, request, view):
        return bool(
            (
                request.method in SAFE_METHODS and
                request.user and request.user.is_authenticated
            )
            or (request.user and request.user.is_staff)
        )


class IsTicketOrderCreatorOrReadOnly(BasePermission):
    """
    Allows only author access to create and view
    """
    def has_permission(self, request, view):
        if view.action == 'create':
            return True
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if view.action == 'create':
            return True
        return obj.user == request.user


class AllowAllPermission(BasePermission):
    def has_permission(self, request, view):
        return True
