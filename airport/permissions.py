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
    Дозволяє доступ для створення тільки автору та дозволяє переглядати усім.
    """
    def has_permission(self, request, view):
        if view.action == 'create':
            return True
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        # Дозволити перегляд тільки автору об'єкта
        if request.method in permissions.SAFE_METHODS:
            return True
        # Дозволити створення тільки автору
        if view.action == 'create':
            return True
        # Перевірка, чи користувач, який робить запит, є автором об'єкта
        return obj.user == request.user


class AllowAllPermission(BasePermission):
    def has_permission(self, request, view):
        return True
