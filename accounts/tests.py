from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.models import User

User = get_user_model()

class AuthenticationTestCase(TestCase):
    def setUp(self):
        """Set up test users"""
        self.client = Client()

        # Create owner user
        self.owner = User.objects.create_user(
            username='owner_test',
            email='owner@test.com',
            password='testpass123',
            first_name='Owner',
            last_name='Test',
            role='owner'
        )

        # Create pegawai user
        self.pegawai = User.objects.create_user(
            username='pegawai_test',
            email='pegawai@test.com',
            password='testpass123',
            first_name='Pegawai',
            last_name='Test',
            role='pegawai'
        )

    def test_home_page_redirects_authenticated_users(self):
        """Test that authenticated users are redirected from home page"""
        # Test owner redirect
        self.client.login(username='owner_test', password='testpass123')
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, reverse('accounts:owner_dashboard'))

        # Test pegawai redirect
        self.client.login(username='pegawai_test', password='testpass123')
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, reverse('accounts:pegawai_dashboard'))

    def test_login_page_access(self):
        """Test that login page is accessible"""
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Money Laundry')

    def test_login_valid_credentials_owner(self):
        """Test login with valid owner credentials"""
        response = self.client.post(reverse('accounts:login'), {
            'username': 'owner_test',
            'password': 'testpass123'
        })
        self.assertRedirects(response, reverse('accounts:owner_dashboard'))

    def test_login_valid_credentials_pegawai(self):
        """Test login with valid pegawai credentials"""
        response = self.client.post(reverse('accounts:login'), {
            'username': 'pegawai_test',
            'password': 'testpass123'
        })
        self.assertRedirects(response, reverse('accounts:pegawai_dashboard'))

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = self.client.post(reverse('accounts:login'), {
            'username': 'wrong_user',
            'password': 'wrong_password'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Username atau password salah')

    def test_dashboard_access_control(self):
        """Test role-based dashboard access control"""
        # Test owner accessing pegawai dashboard (should be redirected to owner dashboard)
        self.client.login(username='owner_test', password='testpass123')
        response = self.client.get(reverse('accounts:pegawai_dashboard'))
        self.assertRedirects(response, reverse('accounts:owner_dashboard'))

        # Test pegawai accessing owner dashboard
        self.client.login(username='pegawai_test', password='testpass123')
        response = self.client.get(reverse('accounts:owner_dashboard'))
        # Should be denied - pegawai cannot access owner dashboard
        self.assertRedirects(response, reverse('home'))

    def test_user_role_methods(self):
        """Test user role helper methods"""
        self.assertTrue(self.owner.is_owner())
        self.assertFalse(self.owner.is_pegawai())

        self.assertTrue(self.pegawai.is_pegawai())
        self.assertFalse(self.pegawai.is_owner())

    def test_logout_functionality(self):
        """Test logout functionality"""
        self.client.login(username='pegawai_test', password='testpass123')
        response = self.client.post(reverse('accounts:logout'))
        self.assertRedirects(response, reverse('accounts:login'))

class UserModelTestCase(TestCase):
    def test_user_creation(self):
        """Test custom user model creation"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='pegawai'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.role, 'pegawai')
        self.assertTrue(user.is_pegawai())
        self.assertFalse(user.is_owner())

    def test_user_str_representation(self):
        """Test user string representation"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            role='pegawai'
        )
        expected_str = f"{user.username} ({user.get_role_display()})"
        self.assertEqual(str(user), expected_str)
