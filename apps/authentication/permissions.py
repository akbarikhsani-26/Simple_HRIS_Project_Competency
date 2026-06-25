from rest_framework import permissions


class IsHRAdmin(permissions.BasePermission):
    """
    Allows access only to HR_ADMIN users.
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == "HR_ADMIN"
        )


class IsEmployeeAndReadOnly(permissions.BasePermission):
    """
    Allows read-only access for EMPLOYEE users.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            and request.user
            and request.user.is_authenticated
            and request.user.role == "EMPLOYEE"
        )


class IsHRAdminOrReadOnlyOwnData(permissions.BasePermission):
    """
    Object-level permission to allow HR_ADMIN full access,
    but EMPLOYEE only read access to their own data.
    """

    def has_object_permission(self, request, view, obj):
        # HR_ADMIN has full permissions
        if request.user.role == "HR_ADMIN":
            return True

        # EMPLOYEE can only read
        if request.method not in permissions.SAFE_METHODS:
            return False

        # Must be their own data
        # Assuming the object has a 'user' attribute linking to the CustomUser
        return hasattr(obj, "user") and obj.user == request.user
