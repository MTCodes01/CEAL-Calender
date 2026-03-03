"""
Tests for the accounts app: signup, login, profile, admin views.
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import User
from clubs.models import Club


class SignupTests(TestCase):
    """Test user registration endpoint."""

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('signup')
        self.valid_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'StrongPass123!',
            'password2': 'StrongPass123!',
            'first_name': 'Test',
            'last_name': 'User',
        }

    def test_signup_success(self):
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='test@example.com').exists())

    def test_signup_password_mismatch(self):
        data = {**self.valid_data, 'password2': 'DifferentPass123!'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_duplicate_email(self):
        self.client.post(self.url, self.valid_data, format='json')
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_weak_password(self):
        data = {**self.valid_data, 'password': '123', 'password2': '123'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTests(TestCase):
    """Test login endpoint."""

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('token_obtain_pair')
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='StrongPass123!',
        )

    def test_login_success(self):
        response = self.client.post(self.url, {
            'email': 'test@example.com',
            'password': 'StrongPass123!',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_wrong_password(self):
        response = self.client.post(self.url, {
            'email': 'test@example.com',
            'password': 'WrongPassword!',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_nonexistent_user(self):
        response = self.client.post(self.url, {
            'email': 'nobody@example.com',
            'password': 'StrongPass123!',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ProfileTests(TestCase):
    """Test user profile endpoint."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='StrongPass123!',
            first_name='Test',
            last_name='User',
        )
        self.client.force_authenticate(user=self.user)

    def test_get_profile(self):
        response = self.client.get(reverse('user-profile'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@example.com')

    def test_update_settings(self):
        response = self.client.put(reverse('user-profile'), {
            'first_name': 'Updated',
            'last_name': 'Name',
            'notification_enabled': False,
            'timezone': 'UTC',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertFalse(self.user.notification_enabled)

    def test_profile_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('user-profile'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ChangePasswordTests(TestCase):
    """Test password change endpoint."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='OldPass123!',
        )
        self.client.force_authenticate(user=self.user)

    def test_change_password_success(self):
        response = self.client.post(reverse('change-password'), {
            'old_password': 'OldPass123!',
            'new_password': 'NewPass456!',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewPass456!'))

    def test_change_password_wrong_old(self):
        response = self.client.post(reverse('change-password'), {
            'old_password': 'WrongOldPass!',
            'new_password': 'NewPass456!',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AdminUserTests(TestCase):
    """Test admin user management endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(
            email='admin@example.com',
            username='admin',
            password='AdminPass123!',
        )
        self.regular_user = User.objects.create_user(
            email='regular@example.com',
            username='regular',
            password='RegularPass123!',
        )

    def test_admin_can_list_users(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_admin_cannot_list_users(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_update_user_club(self):
        club = Club.objects.create(slug='test', name='Test Club', color='#FF0000')
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(
            reverse('user-detail', args=[self.regular_user.id]),
            {'club': club.id},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.regular_user.refresh_from_db()
        self.assertEqual(self.regular_user.club, club)
