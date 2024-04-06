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
