from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

class AllowServiceSeekersAndUnauthenticated(BasePermission):
    """
    Custom permission to allow only service seekers or unauthenticated users.
    """

    def has_permission(self, request, view):
        # Allow access if the user is not authenticated
        if not request.user.is_authenticated:
            return True

        # Allow access if the user is a service seeker
        if hasattr(request.user, 'seeker_profile'):
            return True

        # Otherwise, deny access
        raise PermissionDenied("Only service seekers or unauthenticated users can access this resource.")
