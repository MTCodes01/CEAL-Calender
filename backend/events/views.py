from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.utils.dateparse import parse_datetime
from .models import Event
from .serializers import EventSerializer, EventCreateSerializer
from .permissions import IsClubMemberOrReadOnly, IsSameClubMember


class EventViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Event CRUD operations with club-based permissions
    """
    queryset = Event.objects.select_related('club', 'created_by').all()
    permission_classes = [permissions.IsAuthenticated, IsClubMemberOrReadOnly, IsSameClubMember]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return EventCreateSerializer
        return EventSerializer
    
    def get_queryset(self):
        """
        Filter events by date range if provided in query params
        """
        queryset = super().get_queryset()
        
        # Get query parameters
        start_param = self.request.query_params.get('start', None)
        end_param = self.request.query_params.get('end', None)
        club_ids = self.request.query_params.get('clubs', None)
        
        # Filter by date range (for calendar view)
        if start_param and end_param:
            try:
                start_dt = parse_datetime(start_param)
                end_dt = parse_datetime(end_param)
                
                if start_dt and end_dt:
                    # Query events that overlap with the date range
                    queryset = queryset.filter(
                        start__lte=end_dt,
                        end__gte=start_dt
                    )
            except (ValueError, TypeError):
                pass
        
        # Filter by club IDs
        if club_ids:
            club_id_list = [int(cid) for cid in club_ids.split(',') if cid.isdigit()]
            if club_id_list:
                queryset = queryset.filter(club_id__in=club_id_list)
        
        return queryset
    
    def perform_create(self, serializer):
        """
        Auto-fill club and created_by from current user
        """
        if not self.request.user.club:
            raise permissions.PermissionDenied("You must be a member of a club to create events.")
        
        serializer.save(
            club=self.request.user.club,
            created_by=self.request.user
        )
    
    def perform_update(self, serializer):
        """
        Ensure club cannot be changed during update
        """
        serializer.save(club=serializer.instance.club, created_by=serializer.instance.created_by)
