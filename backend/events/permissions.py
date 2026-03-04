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
    Strict RBAC for events:
    - Super Admin: All permissions.
    - Club Admin: Can only add/edit/delete events for their specific club.
    - Sub-Club Admin: Can only add/edit/delete events for their specific sub-club.
    - No Role: Read-only access.
    """
    def has_permission(self, request, view):
        # Read permissions for all authenticated users
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Super admin can do anything
        if request.user.is_superuser:
            return True
            
        # For POST (create), check if user has a club or sub_club
        if request.method == 'POST':
            return request.user.club is not None or request.user.sub_club is not None
            
        return True # Handled by has_object_permission for PUT/PATCH/DELETE

    def has_object_permission(self, request, view, obj):
        # Read permissions for all authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Super admin can do anything
        if request.user.is_superuser:
            return True
        
        # Check sub_club first (more specific role)
        # If user has a sub_club role, they can ONLY manage events FOR THAT sub_club
        if request.user.sub_club:
            return obj.club.id == request.user.sub_club.id
            
        # Then check main club role
        # If user has a main club role, they can manage events FOR THAT club
        # AND events for any of its sub-clubs
        if request.user.club:
            # Check if the event belongs to the main club
            if obj.club.id == request.user.club.id:
                return True
            # Check if the event's club is a sub-club of the user's club
            if obj.club.parent and obj.club.parent.id == request.user.club.id:
                return True
            
        return False
