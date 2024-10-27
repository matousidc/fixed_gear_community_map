from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib import auth
from django.urls import reverse
from map.models import UserProfiles


class UserLoginTest(TestCase):

    def setUp(self):
        # Create a user for testing login
        self.user = User.objects.create_user(username='testuser', email='Jq7u8@example.com', password='testpassword')
        self.user_profile = UserProfiles.objects.create(user=self.user)
        self.login_url = reverse('login')  # Assuming the login URL is named 'login'

    def test_login_with_valid_credentials(self):
        # Test login with valid credentials
        login_data = {'email': 'Jq7u8@example.com', 'password': 'testpassword'}
        response = self.client.post(self.login_url, login_data)
        user = auth.get_user(self.client)
        # Check that the login was successful
        self.assertEqual(response.status_code, 302)  # Expecting a redirect on successful login
        self.assertRedirects(response, reverse('profile'))  # Assuming successful login redirects to 'profile'
        self.assertTrue(user.is_authenticated)
        self.assertTrue(
            self.client.login(username='testuser',
                              password=login_data['password']))  # Verifying login

    def test_login_with_invalid_password(self):
        # Test login with invalid credentials
        login_data = {'email': 'Jq7u8@example.com', 'password': 'wrongpassword'}
        response = self.client.post(self.login_url, login_data)
        # Check that the login failed
        self.assertEqual(response.status_code, 200)  # Should stay on the login page
        self.assertContains(response, "Wrong password.")  # Error message displayed
        self.assertFalse(
            self.client.login(username='testuser',
                              password=login_data['password']))  # Login should fail

    def test_login_with_invalid_email(self):
        # Test login with invalid credentials
        login_data = {'email': 'invalidemail@abc.com', 'password': 'testpassword'}
        response = self.client.post(self.login_url, login_data)
        # Check that the login failed
        self.assertEqual(response.status_code, 200)  # Should stay on the login page
        self.assertContains(response, "User with this email")  # Error message displayed


class UserSignupTest(TestCase):

    def setUp(self):
        self.signup_url = reverse('signup')  # Assuming the login URL is named 'login'

    def test_signup_with_valid_credentials(self):
        # Test login with valid credentials
        signup_data = {'email': 'Jq7u8@example.com', 'password1': 'testpassword', 'password2': 'testpassword'}
        response = self.client.post(self.signup_url, signup_data)
        user = auth.get_user(self.client)
        self.assertEqual(response.status_code, 302)  # Expecting a redirect on successful login
        self.assertRedirects(response, reverse('create-profile'))  # successful signup redirects to 'create-profile'
        self.assertTrue(user.is_authenticated)

    def test_signup_with_different_passwords(self):
        # Test login with invalid credentials
        signup_data = {'email': 'Jq7u8@example.com', 'password1': 'testpassword', 'password2': 'wrongpassword'}
        response = self.client.post(self.signup_url, signup_data)
        self.assertEqual(response.status_code, 200)  # Should stay on the signup page
        self.assertContains(response, 'Passwords do not match.')  # Error message displayed

    def test_signup_with_existing_email(self):
        # Test login with invalid credentials
        User.objects.create_user(username='testuser', email='Jq7u8@example.com', password='testpassword')
        signup_data = {'email': 'Jq7u8@example.com', 'password1': 'testpassword', 'password2': 'testpassword'}
        response = self.client.post(self.signup_url, signup_data)
        self.assertEqual(response.status_code, 200)  # Should stay on the signup page
        self.assertContains(response, 'User with this email already exists.')  # Error message displayed


class LogoutTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='Jq7u8@example.com', password='testpassword')
        self.login_url = reverse('login')  # Assuming the login URL is named 'login'
        login_data = {'email': 'Jq7u8@example.com', 'password': 'testpassword'}
        self.client.post(self.login_url, login_data)
        self.logout_url = reverse('logout')  # Assuming the logout URL is named 'logout'

    def test_logout(self):
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)
        user = auth.get_user(self.client)
        self.assertRedirects(response, reverse('login'))
        self.assertFalse(user.is_authenticated)
        self.assertFalse(self.client.session.get('_auth_user_id'))
