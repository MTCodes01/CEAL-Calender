from rest_framework import generics, permissions, viewsets
from .models import Club
from .serializers import ClubSerializer


class ClubListView(generics.ListAPIView):
    """
    List all main clubs with their sub-clubs (public endpoint)
    """
    serializer_class = ClubSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        # Only return main clubs (no parent) and order by the new order field
        return Club.objects.filter(parent__isnull=True).order_by('order', 'name')


class ClubManagementViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Super Admin to manage clubs and sub-clubs
    """
    queryset = Club.objects.all().order_by('order', 'name')
    serializer_class = ClubSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        # Super admin only
        serializer.save()
