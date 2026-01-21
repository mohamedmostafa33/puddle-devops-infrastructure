"""
Unit tests for Puddle Core app
Tests authentication, user registration, and basic views
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class CoreViewsTestCase(TestCase):
    """Test core application views"""

    def setUp(self):
        """Set up test client and test user"""
        self.client = Client()
        self.test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_index_page_loads(self):
        """Test that index page loads successfully"""
        response = self.client.get(reverse('core:index'))
        self.assertEqual(response.status_code, 200)

    def test_signup_page_loads(self):
        """Test that signup page loads"""
        response = self.client.get(reverse('core:signup'))
        self.assertEqual(response.status_code, 200)

    def test_login_page_loads(self):
        """Test that login page loads"""
        response = self.client.get(reverse('core:login'))
        self.assertEqual(response.status_code, 200)

    def test_user_can_login(self):
        """Test user authentication"""
        login_successful = self.client.login(
            username='testuser',
            password='testpass123'
        )
        self.assertTrue(login_successful)

    def test_contact_page_loads(self):
        """Test contact page loads"""
        response = self.client.get(reverse('core:contact'))
        self.assertEqual(response.status_code, 200)


class UserAuthenticationTestCase(TestCase):
    """Test user authentication flows"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='authuser',
            password='authpass123'
        )

    def test_login_with_valid_credentials(self):
        """Test login with correct credentials"""
        response = self.client.post(reverse('core:login'), {
            'username': 'authuser',
            'password': 'authpass123'
        })
        self.assertEqual(response.status_code, 302)

    def test_logout(self):
        """Test user logout"""
        self.client.login(username='authuser', password='authpass123')
        response = self.client.post(reverse('core:logout'))
        self.assertEqual(response.status_code, 302)
