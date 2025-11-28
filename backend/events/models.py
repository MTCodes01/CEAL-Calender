from django.db import models
from django.conf import settings
from clubs.models import Club


class Event(models.Model):
    """
    Event model with full datetime support and location
    Supports overlapping events at different locations
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # Full datetime support (not just dates)
    start = models.DateTimeField()
    end = models.DateTimeField()
    
    # Location support for overlapping events
    location = models.CharField(max_length=255, help_text="Event location (e.g., 'CS Lab 2', 'Main Auditorium')")
    
    # Relations
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='events')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_events')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['start']
        indexes = [
            models.Index(fields=['start', 'end']),
            models.Index(fields=['club', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.club.name}) - {self.start.strftime('%Y-%m-%d %H:%M')}"
