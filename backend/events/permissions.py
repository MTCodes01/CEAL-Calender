from rest_framework import permissions


class IsClubMemberOrReadOnly(permissions.BasePermission):
    """
    Only club members can create events.
    Read-only access for all authenticated users.
    """
    def has_permission(self, request, view):
        # Read permissions for all authenticated users
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Write permissions only for users with a club
        return request.user and request.user.is_authenticated and request.user.club is not None


class IsSameClubMember(permissions.BasePermission):
    """
    Only members of the same club can edit/delete events.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions for all authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only for users in the same club
        if not request.user or not request.user.is_authenticated:
            return False
            
        if request.user.is_superuser:
            return True
        
        # Check sub_club first (more specific)
        if request.user.sub_club:
            return obj.club == request.user.sub_club
            
        # Then check main club
        if request.user.club:
            return obj.club == request.user.club
            
        return False
