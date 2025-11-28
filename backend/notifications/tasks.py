from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
from datetime import datetime
from accounts.models import User
from events.models import Event
from .utils import convert_to_local, is_within_minute, format_event_datetime


@shared_task
def dispatch_notifications():
    """
    Celery task to dispatch email notifications to users
    Runs every minute via Celery Beat
    
    Logic:
    1. Get all users with notification_enabled=True
    2. For each user, check if current local time matches notification_time
    3. Query for new events created since last_notification_sent_at
    4. If new events exist, send email and update last_notification_sent_at
    """
    now_utc = timezone.now()
    users = User.objects.filter(notification_enabled=True, notification_time__isnull=False)
    
    sent_count = 0
    
    for user in users:
        try:
            # Convert current UTC time to user's local timezone
            local_now = convert_to_local(now_utc, user.timezone)
            
            # Check if current local time matches user's notification time
            if not is_within_minute(local_now.time(), user.notification_time):
                continue
            
            # Get timestamp of last notification (default to epoch if never sent)
            last_sent = user.last_notification_sent_at or timezone.make_aware(datetime(1970, 1, 1))
            
            # Query for new events created since last notification
            # Only events from the user's club
            if not user.club:
                continue
            
            new_events = Event.objects.filter(
                created_at__gt=last_sent,
                club=user.club
            ).select_related('club', 'created_by').order_by('start')
            
            if not new_events.exists():
                continue
            
            # Send email with new events
            success = send_digest_email(user, new_events)
            
            if success:
                # Update last notification timestamp
                user.last_notification_sent_at = now_utc
                user.save(update_fields=['last_notification_sent_at'])
                sent_count += 1
        
        except Exception as e:
            # Log error but continue processing other users
            print(f"Error sending notification to {user.email}: {str(e)}")
            continue
    
    return f"Sent {sent_count} notification(s)"


def send_digest_email(user, events):
    """
    Send HTML email digest with new events to user
    
    Args:
        user: User object
        events: QuerySet of Event objects
    
    Returns:
        bool: True if email sent successfully
    """
    try:
        # Prepare event data for template
        event_data = []
        for event in events:
            event_data.append({
                'title': event.title,
                'description': event.description,
                'datetime': format_event_datetime(event.start, user.timezone),
                'end_datetime': format_event_datetime(event.end, user.timezone),
                'location': event.location,
                'created_by': f"{event.created_by.first_name} {event.created_by.last_name}".strip() or event.created_by.username,
            })
        
        # Render HTML email
        html_content = render_to_string('email_digest.html', {
            'user': user,
            'club_name': user.club.name,
            'events': event_data,
            'event_count': len(event_data),
            'frontend_url': settings.FRONTEND_URL,
        })
        
        # Send email
        send_mail(
            subject=f"New Events in {user.club.name}",
            message=f"You have {len(event_data)} new event(s) in {user.club.name}. Visit {settings.FRONTEND_URL} to view details.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_content,
            fail_silently=False,
        )
        
        return True
    
    except Exception as e:
        print(f"Failed to send email to {user.email}: {str(e)}")
        return False
