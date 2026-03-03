"""
Tests for the events app: CRUD, permissions, date filtering.
"""
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from datetime import timedelta
from accounts.models import User
from clubs.models import Club
from events.models import Event


class EventCRUDTests(TestCase):
    """Test event create, read, update, delete."""

    def setUp(self):
        self.client = APIClient()
        self.club = Club.objects.create(slug='cs', name='CS Club', color='#3B82F6')
        self.other_club = Club.objects.create(slug='ee', name='EE Club', color='#EF4444')
        self.user = User.objects.create_user(
            email='member@example.com',
            username='member',
            password='Pass123!',
            club=self.club,
        )
        self.other_user = User.objects.create_user(
            email='other@example.com',
            username='othermember',
            password='Pass123!',
            club=self.other_club,
        )
        self.client.force_authenticate(user=self.user)
        self.now = timezone.now()

    def _create_event(self, user=None, club=None):
        """Helper to create a test event."""
        return Event.objects.create(
            title='Test Event',
            description='A test event',
            start=self.now + timedelta(hours=1),
            end=self.now + timedelta(hours=2),
            location='CS Lab 1',
            club=club or self.club,
            created_by=user or self.user,
        )

    def test_create_event(self):
        response = self.client.post(reverse('event-list'), {
            'title': 'New Event',
            'description': 'Description',
            'start': (self.now + timedelta(hours=1)).isoformat(),
            'end': (self.now + timedelta(hours=2)).isoformat(),
            'location': 'Main Hall',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 1)
        event = Event.objects.first()
        self.assertEqual(event.club, self.club)
        self.assertEqual(event.created_by, self.user)

    def test_create_event_without_club(self):
        """Users without a club cannot create events."""
        no_club_user = User.objects.create_user(
            email='noclubuser@example.com',
            username='noclubuser',
            password='Pass123!',
        )
        self.client.force_authenticate(user=no_club_user)
        response = self.client.post(reverse('event-list'), {
            'title': 'New Event',
            'start': (self.now + timedelta(hours=1)).isoformat(),
            'end': (self.now + timedelta(hours=2)).isoformat(),
            'location': 'Main Hall',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_read_events(self):
        self._create_event()
        response = self.client.get(reverse('event-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_own_club_event(self):
        event = self._create_event()
        response = self.client.put(
            reverse('event-detail', args=[event.id]),
            {
                'title': 'Updated Title',
                'description': 'Updated',
                'start': event.start.isoformat(),
                'end': event.end.isoformat(),
                'location': 'Updated Location',
            },
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        event.refresh_from_db()
        self.assertEqual(event.title, 'Updated Title')

    def test_cannot_update_other_club_event(self):
        event = self._create_event(user=self.other_user, club=self.other_club)
        response = self.client.put(
            reverse('event-detail', args=[event.id]),
            {
                'title': 'Hacked Title',
                'start': event.start.isoformat(),
                'end': event.end.isoformat(),
                'location': 'Hacked',
            },
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_own_club_event(self):
        event = self._create_event()
        response = self.client.delete(reverse('event-detail', args=[event.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Event.objects.count(), 0)

    def test_cannot_delete_other_club_event(self):
        event = self._create_event(user=self.other_user, club=self.other_club)
        response = self.client.delete(reverse('event-detail', args=[event.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser_can_edit_any_event(self):
        admin = User.objects.create_superuser(
            email='admin@example.com',
            username='admin',
            password='Admin123!',
        )
        event = self._create_event(user=self.other_user, club=self.other_club)
        self.client.force_authenticate(user=admin)
        response = self.client.put(
            reverse('event-detail', args=[event.id]),
            {
                'title': 'Admin Updated',
                'start': event.start.isoformat(),
                'end': event.end.isoformat(),
                'location': 'Admin Location',
            },
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class EventValidationTests(TestCase):
    """Test event data validation."""

    def setUp(self):
        self.client = APIClient()
        self.club = Club.objects.create(slug='cs', name='CS Club', color='#3B82F6')
        self.user = User.objects.create_user(
            email='member@example.com',
            username='member',
            password='Pass123!',
            club=self.club,
        )
        self.client.force_authenticate(user=self.user)
        self.now = timezone.now()

    def test_end_before_start_rejected(self):
        response = self.client.post(reverse('event-list'), {
            'title': 'Bad Event',
            'start': (self.now + timedelta(hours=2)).isoformat(),
            'end': (self.now + timedelta(hours=1)).isoformat(),
            'location': 'Lab',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class EventFilteringTests(TestCase):
    """Test date range and club filtering."""

    def setUp(self):
        self.client = APIClient()
        self.club1 = Club.objects.create(slug='cs', name='CS Club', color='#3B82F6')
        self.club2 = Club.objects.create(slug='ee', name='EE Club', color='#EF4444')
        self.user = User.objects.create_user(
            email='member@example.com',
            username='member',
            password='Pass123!',
            club=self.club1,
        )
        self.client.force_authenticate(user=self.user)
        self.now = timezone.now()

        # Create events in different time ranges
        Event.objects.create(
            title='Past Event', start=self.now - timedelta(days=10),
            end=self.now - timedelta(days=9), location='Room 1',
            club=self.club1, created_by=self.user,
        )
        Event.objects.create(
            title='Current Event', start=self.now - timedelta(hours=1),
            end=self.now + timedelta(hours=1), location='Room 2',
            club=self.club1, created_by=self.user,
        )
        Event.objects.create(
            title='Future Event', start=self.now + timedelta(days=10),
            end=self.now + timedelta(days=11), location='Room 3',
            club=self.club2, created_by=self.user,
        )

    def test_filter_by_date_range(self):
        start = (self.now - timedelta(days=1)).isoformat()
        end = (self.now + timedelta(days=1)).isoformat()
        response = self.client.get(reverse('event-list'), {'start': start, 'end': end})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should only include the current event
        titles = [e['title'] for e in (response.data if isinstance(response.data, list) else response.data.get('results', []))]
        self.assertIn('Current Event', titles)
        self.assertNotIn('Past Event', titles)

    def test_filter_by_club(self):
        response = self.client.get(reverse('event-list'), {'clubs': str(self.club2.id)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data if isinstance(response.data, list) else response.data.get('results', [])
        for event in results:
            self.assertEqual(event['club']['id'], self.club2.id)
