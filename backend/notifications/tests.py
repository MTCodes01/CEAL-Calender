"""
Tests for the notifications app: dispatch logic, batching, utilities.
"""
from datetime import time, datetime, timedelta
from unittest.mock import patch, MagicMock

from django.test import TestCase
from django.utils import timezone

from accounts.models import User
from clubs.models import Club
from events.models import Event
from notifications.utils import is_within_minute, is_notification_due_today, convert_to_local, format_event_datetime


class IsWithinMinuteTests(TestCase):
    """Test the is_within_minute utility."""

    def test_same_time(self):
        t = time(9, 30)
        self.assertTrue(is_within_minute(t, t))

    def test_different_seconds_same_minute(self):
        t1 = time(9, 30, 0)
        t2 = time(9, 30, 45)
        self.assertTrue(is_within_minute(t1, t2))

    def test_different_minutes(self):
        t1 = time(9, 30)
        t2 = time(9, 31)
        self.assertFalse(is_within_minute(t1, t2))

    def test_none_values(self):
        self.assertFalse(is_within_minute(None, time(9, 30)))
        self.assertFalse(is_within_minute(time(9, 30), None))
        self.assertFalse(is_within_minute(None, None))


class IsNotificationDueTodayTests(TestCase):
    """Test the is_notification_due_today fallback checker."""

    def test_due_never_sent(self):
        """Notification is due if never sent and time has passed."""
        import pytz
        tz_str = 'Asia/Kolkata'
        tz = pytz.timezone(tz_str)
        local_now = datetime(2025, 6, 15, 10, 0, tzinfo=tz)
        notif_time = time(9, 0)
        result = is_notification_due_today(local_now, notif_time, None, tz_str)
        self.assertTrue(result)

    def test_not_due_before_time(self):
        """Not due if current time is before notification time."""
        import pytz
        tz_str = 'Asia/Kolkata'
        tz = pytz.timezone(tz_str)
        local_now = datetime(2025, 6, 15, 8, 0, tzinfo=tz)
        notif_time = time(9, 0)
        result = is_notification_due_today(local_now, notif_time, None, tz_str)
        self.assertFalse(result)

    def test_not_due_already_sent_today(self):
        """Not due if already sent today."""
        import pytz
        tz_str = 'Asia/Kolkata'
        tz = pytz.timezone(tz_str)
        local_now = datetime(2025, 6, 15, 10, 0, tzinfo=tz)
        notif_time = time(9, 0)
        # Last sent earlier today in UTC
        last_sent = timezone.make_aware(datetime(2025, 6, 15, 4, 0), pytz.UTC)
        result = is_notification_due_today(local_now, notif_time, last_sent, tz_str)
        self.assertFalse(result)


class ConvertToLocalTests(TestCase):
    """Test timezone conversion utility."""

    def test_valid_timezone(self):
        import pytz
        utc_time = timezone.make_aware(datetime(2025, 6, 15, 0, 0), pytz.UTC)
        local = convert_to_local(utc_time, 'Asia/Kolkata')
        self.assertEqual(local.hour, 5)  # UTC+5:30
        self.assertEqual(local.minute, 30)

    def test_invalid_timezone_fallback(self):
        import pytz
        utc_time = timezone.make_aware(datetime(2025, 6, 15, 0, 0), pytz.UTC)
        local = convert_to_local(utc_time, 'Invalid/Timezone')
        self.assertEqual(local, utc_time)


class DispatchNotificationsTests(TestCase):
    """Test the dispatch_notifications task logic."""

    def setUp(self):
        self.club_a = Club.objects.create(slug='cs', name='CS Club', color='#3B82F6')
        self.club_b = Club.objects.create(slug='ai', name='AI Club', color='#10B981')

        self.creator = User.objects.create_user(
            email='admin@cs.com',
            username='admin',
            password='Pass123!',
            club=self.club_a,
            notification_enabled=False,
        )

        self.user_a = User.objects.create_user(
            email='member_a@cs.com',
            username='member_a',
            password='Pass123!',
            club=self.club_a,
            notification_enabled=True,
            notification_time=time(9, 0),
            timezone='UTC',
        )

        self.user_no_club = User.objects.create_user(
            email='noclub@example.com',
            username='noclub',
            password='Pass123!',
            club=None,
            notification_enabled=True,
            notification_time=time(9, 0),
            timezone='UTC',
        )

        self.now = timezone.now()

    @patch('notifications.tasks.send_digest_email', return_value=True)
    def test_user_gets_events_added_recently_from_other_clubs(self, mock_send):
        """
        Users get notified about newly added events from ANY club in the 24h window before notification.
        """
        # Event created just now
        Event.objects.create(
            title='AI Workshop',
            start=self.now + timedelta(days=10), # Start time doesn't matter
            end=self.now + timedelta(days=10, hours=1),
            location='Lab B',
            club=self.club_b,
            created_by=self.creator,
        )
        for user in [self.user_a, self.user_no_club]:
            user.notification_time = time(self.now.hour, self.now.minute)
            user.save()

        from notifications.tasks import dispatch_notifications
        result = dispatch_notifications()

        self.assertEqual(mock_send.call_count, 2)
        self.assertIn('2 notification', result)

    @patch('notifications.tasks.send_digest_email', return_value=True)
    def test_events_added_outside_24h_window_excluded(self, mock_send):
        """Events added > 24h ago should NOT be notified."""
        event = Event.objects.create(
            title='Old Event',
            start=self.now + timedelta(days=5),
            end=self.now + timedelta(days=5, hours=1),
            location='Main Hall',
            club=self.club_a,
            created_by=self.creator,
        )
        # Manually backdate updated_at using update()
        Event.objects.filter(pk=event.pk).update(updated_at=self.now - timedelta(hours=30))

        self.user_a.notification_time = time(self.now.hour, self.now.minute)
        self.user_a.save()
        self.user_no_club.notification_enabled = False
        self.user_no_club.save()

        from notifications.tasks import dispatch_notifications
        result = dispatch_notifications()

        mock_send.assert_not_called()

    @patch('notifications.tasks.send_digest_email', return_value=True)
    def test_updated_event_triggers_notification(self, mock_send):
        """An event updated in the last 24h (after old notification) triggers."""
        event = Event.objects.create(
            title='Meeting',
            start=self.now + timedelta(days=5),
            end=self.now + timedelta(days=5, hours=1),
            location='Room 5',
            club=self.club_a,
            created_by=self.creator,
        )
        # updated_at is now, but last notification was 2 hours ago
        self.user_a.last_notification_sent_at = self.now - timedelta(hours=2)
        self.user_a.notification_time = time(self.now.hour, self.now.minute)
        self.user_a.save()
        self.user_no_club.notification_enabled = False
        self.user_no_club.save()

        from notifications.tasks import dispatch_notifications
        result = dispatch_notifications()

        mock_send.assert_called_once()
        args = mock_send.call_args[0]
        # Check that the event is in the list of events passed to send_digest_email
        event_list = args[1]
        self.assertIn(event, event_list)

    @patch('notifications.tasks.send_digest_email', return_value=True)
    def test_no_dispatch_without_events_in_added_window(self, mock_send):
        """No notifications when there are no newly added events."""
        self.user_a.notification_time = time(self.now.hour, self.now.minute)
        self.user_a.last_notification_sent_at = self.now
        self.user_a.save()
        self.user_no_club.notification_enabled = False
        self.user_no_club.save()

        from notifications.tasks import dispatch_notifications
        result = dispatch_notifications()
        mock_send.assert_not_called()
