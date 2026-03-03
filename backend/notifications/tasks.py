import logging
from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
from datetime import datetime

import pytz

from accounts.models import User
from events.models import Event
from .utils import convert_to_local, is_within_minute, is_notification_due_today, format_event_datetime

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=60,
    retry_backoff_max=300,
    max_retries=3,
)
def dispatch_notifications(self):
    """
    Celery task to dispatch email notifications to users.
    Runs every minute via Celery Beat.

    Sends ALL users with notifications enabled a digest of events
    from ANY club, as long as:
      1. It is the user's notification time (or overdue today).
      2. The event was added or updated in the 24 hours preceding the notification.
    """
    now_utc = timezone.now()

    # All users who have opted into notifications (no club requirement)
    users = (
        User.objects
        .filter(notification_enabled=True, notification_time__isnull=False)
        .select_related('club', 'sub_club')
    )

    # ---------------------------------------------------------------
    # Step 1: Determine which users are eligible RIGHT NOW
    # ---------------------------------------------------------------
    eligible_users = []
    for user in users:
        try:
            local_now = convert_to_local(now_utc, user.timezone)

            # Primary check: exact minute match
            if is_within_minute(local_now.time(), user.notification_time):
                eligible_users.append(user)
                continue

            # Fallback: notification is due today but hasn't been sent
            if is_notification_due_today(local_now, user.notification_time, user.last_notification_sent_at, user.timezone):
                eligible_users.append(user)
        except Exception as e:
            logger.error("Error checking eligibility for user %s: %s", user.email, e)

    if not eligible_users:
        return "No users eligible for notification at this time."

    logger.info("Found %d eligible user(s) for notification dispatch.", len(eligible_users))

    # ---------------------------------------------------------------
    # Step 2: Send notification to each eligible user
    # ---------------------------------------------------------------
    sent_count = 0
    for user in eligible_users:
        try:
            user_last_sent = user.last_notification_sent_at or timezone.make_aware(datetime(1970, 1, 1))

            # Compute the user's notification datetime for today (in their timezone)
            try:
                user_tz = pytz.timezone(user.timezone)
            except Exception:
                user_tz = pytz.UTC

            local_now = convert_to_local(now_utc, user.timezone)
            notif_today = user_tz.localize(
                datetime.combine(local_now.date(), user.notification_time)
            )

            # Determine the 24-hour window before the user's notification time today
            window_start = notif_today - timedelta(hours=24)
            window_start_utc = window_start.astimezone(pytz.UTC)

            # Effective start is whichever is more recent: the user's last notification time,
            # or 24 hours ago (prevents spamming all historical events on the first day).
            effective_start_utc = max(window_start_utc, user_last_sent)

            # Query events across ALL clubs that:
            # - Were added or updated in the 24h period before the notification
            new_events = list(
                Event.objects
                .filter(
                    updated_at__gt=effective_start_utc,
                    updated_at__lte=now_utc
                )
                .select_related('club', 'created_by')
                .order_by('start')
            )

            if not new_events:
                logger.debug("No relevant events for user %s.", user.email)
                continue

            logger.info(
                "Sending %d event(s) to user %s.",
                len(new_events), user.email
            )

            success = send_digest_email(user, new_events)
            if success:
                user.last_notification_sent_at = now_utc
                user.save(update_fields=['last_notification_sent_at'])
                sent_count += 1

        except Exception as e:
            logger.error("Error processing notification for %s: %s", user.email, e, exc_info=True)

    result = f"Sent {sent_count} notification(s)"
    logger.info(result)
    return result


def send_digest_email(user, events):
    """
    Send HTML email digest with upcoming events to a user.

    Args:
        user: User object
        events: list of Event objects (from any club)

    Returns:
        bool: True if email sent successfully
    """
    try:
        # Prepare event data for template
        event_data = []
        for event in events:
            event_data.append({
                'title': event.title,
                'club_name': event.club.name,
                'description': event.description,
                'datetime': format_event_datetime(event.start, user.timezone),
                'end_datetime': format_event_datetime(event.end, user.timezone),
                'location': event.location,
                'created_by': f"{event.created_by.first_name} {event.created_by.last_name}".strip() or event.created_by.username,
            })

        # Render HTML email
        html_content = render_to_string('email_digest.html', {
            'user': user,
            'events': event_data,
            'event_count': len(event_data),
            'frontend_url': settings.FRONTEND_URL,
        })

        # Send email
        send_mail(
            subject=f"Upcoming Events – CEAL Calendar",
            message=(
                f"You have {len(event_data)} upcoming event(s) across clubs. "
                f"Visit {settings.FRONTEND_URL} to view details."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_content,
            fail_silently=False,
        )

        logger.info("Digest email sent to %s (%d events)", user.email, len(event_data))
        return True

    except Exception as e:
        logger.error("Failed to send email to %s: %s", user.email, e, exc_info=True)
        return False
