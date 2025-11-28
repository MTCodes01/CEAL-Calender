from rest_framework import generics, permissions
from .models import Club
from .serializers import ClubSerializer


class ClubListView(generics.ListAPIView):
    """
    List all clubs (public endpoint for signup and filtering)
    """
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    permission_classes = [permissions.AllowAny]
