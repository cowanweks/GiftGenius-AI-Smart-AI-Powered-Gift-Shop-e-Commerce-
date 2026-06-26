from rest_framework import permissions


class IsVendor(permissions.BasePermission):
    """Allows access only to authenticated vendor (company) accounts."""

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.is_vendor)


class IsApprovedVendor(IsVendor):
    """A vendor whose company has been approved by an admin."""

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        company = getattr(request.user, 'company', None)
        return bool(company and company.status == 'approved')
