from django.contrib.auth.models import AbstractUser
from django.db import models
from clubs.models import Club


class User(AbstractUser):
    """
    Custom User model with club affiliation and notification preferences
    """
    email = models.EmailField(unique=True)
    club = models.ForeignKey(
        Club,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='members'
    )
    sub_club = models.ForeignKey(
        Club,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='sub_club_members'
    )
    
    # Notification settings
    notification_enabled = models.BooleanField(default=True)
    notification_time = models.TimeField(
        null=True,
        blank=True,
        help_text="Time to send daily notification (in user's timezone)"
    )
    timezone = models.CharField(
        max_length=64,
        default="Asia/Kolkata",
        help_text="User's timezone (e.g., 'Asia/Kolkata', 'America/New_York')"
    )
    last_notification_sent_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="UTC timestamp of last notification sent"
    )
    
    # Use email as username field for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        ordering = ['email']
    
    def __str__(self):
        return self.email
