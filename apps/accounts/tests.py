"""Tests for accounts app."""
from django.test import TestCase
from django.shortcuts import reverse
from accounts.forms import CustomUserAuthenticationForm
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import login

# Create your tests here.


class LoginGETTest(TestCase):
    """This tests the login view."""

    def setUp(self):
        """Set things up for testing login functionality."""
        self.url = reverse('accounts:login')
        self.response = self.client.get(self.url)

    def test_csrf(self):
        """Test for csrf token."""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        """Tests if it contains form."""
        form = self.response.context.get('form')
        self.assertIsInstance(form, CustomUserAuthenticationForm)

    def test_response_status_code(self):
        """Tests for `OK` response."""
        self.assertEqual(self.response.status_code, 200)

    def test_login_view_is_rendered(self):
        """Tests if `accounts/login.html` and `base.html` is used."""
        self.assertTemplateUsed(self.response, 'accounts/login.html')
        self.assertTemplateUsed(self.response, 'base.html')

    def test_contains_signup_link(self):
        """Test if it contains `signup` link."""
        # TODO: Change this to test for actual link
        self.assertContains(self.response, 'href="#signup"')

    def test_contains_forgot_password_link(self):
        """Test if it contains `forgot_password` link."""
        # TODO: Change this to test for actual link
        self.assertContains(self.response, 'href="#forgot_password"')
    
    def test_form_inputs(self):
        '''
        The view must contain three inputs: csrf, username, password.
        '''
        self.assertContains(self.response, '<input', 3)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="password"', 1)


class LoginPostTest(TestCase):
    def setUp(self):
        self.url = reverse('accounts:login')
        self.user = User.objects.create_user('foo', 'mail@example.com', 'bar')

    def test_empty_password_post_data(self):
        data = {
            'username': self.user.username,
            'password': '', # Empty password
        }
        response = self.client.post(self.url, data)

        # Assert that the form has error
        error_message = ['This field is required.']
        self.assertFormError(response, 'form', 'password', error_message)

        # Test that the user is not logged in.
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated())

        # Test that the template is same
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'accounts/login.html')

        # Test that the redirect doesnot occur. Redirect occurs after successful login.
        self.assertEqual(response.status_code,200)
        self.assertNotEqual(response.status_code, 302)

    def test_wrong_user_password_post_data(self):
        data = {
            'username': self.user.username,
            'password': 'foobar', # Wrong password data
        }
        # Send post data to client.
        response = self.client.post(self.url, data)

        # Test that the redirect doesnot occur. Redirect occurs after successful login.
        self.assertEqual(response.status_code,200)
        self.assertNotEqual(response.status_code, 302)

        # Assert that the form has error
        error_message = 'Please enter a correct username and password. ' 'Note that both fields may be case-sensitive.'
        self.assertFormError(response, 'form', None, error_message)

        # Test that the template is same
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'accounts/login.html')

        # Test that the user is not logged in.
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated())

    def test_successfull_post_login_data(self):
        data = {
            'username': self.user.username,
            'password': 'bar',  # Correct password
        }

        # Send post data to client.
        response = self.client.post(self.url, data)

        # Test that the redirect doesnot occur. Redirect occurs after successful login.
        self.assertRedirects(response, expected_url=reverse(settings.LOGIN_REDIRECT_URL), status_code=302)
        # TODO: Test for `?next=` also.

        # Test that the template isnot used. Because, it must be a redirection.
        self.assertTemplateNotUsed(response, 'base.html')
        self.assertTemplateNotUsed(response, 'accounts/login.html')

        # Test that the user is not logged in.
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated())
    
    def test_successfull_post_login_redirects_next(self):
        data = {
            'username': self.user.username,
            'password': 'bar',  # Correct password
        }

        # Send post data to client.
        response = self.client.post(self.url+'?next='+reverse('Home'), data)

        # Test that the redirect doesnot occur. Redirect occurs after successful login.
        self.assertRedirects(response, expected_url=reverse('Home'), status_code=302)
        # TODO: Test for `?next=` also.

        # Test that the template isnot used. Because, it must be a redirection.
        self.assertTemplateNotUsed(response, 'base.html')
        self.assertTemplateNotUsed(response, 'accounts/login.html')

        # Test that the user is not logged in.
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated())

    def test_empty_username_post_data(self):
        data = {
            'username': '',
            'password': 'bababa', # Empty password
        }
        response = self.client.post(self.url, data)

        # Assert that the form has error
        error_message = ['This field is required.']
        self.assertFormError(response, 'form', 'username', error_message)

        # Test that the user is not logged in.
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated())

        # Test that the template is same
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'accounts/login.html')

        # Test that the redirect doesnot occur. Redirect occurs after successful login.
        self.assertEqual(response.status_code,200)
        self.assertNotEqual(response.status_code, 302)

    def test_wrong_username_post_data(self):
        data = {
            'username': 'fppnar',
            'password': 'foobar', # Wrong password data
        }
        # Send post data to client.
        response = self.client.post(self.url, data)

        # Test that the redirect doesnot occur. Redirect occurs after successful login.
        self.assertEqual(response.status_code,200)
        self.assertNotEqual(response.status_code, 302)

        # Assert that the form has error
        error_message = 'Please enter a correct username and password. ' 'Note that both fields may be case-sensitive.'
        self.assertFormError(response, 'form', None, error_message)

        # Test that the template is same
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'accounts/login.html')

        # Test that the user is not logged in.
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated())


class UnverifiedEmailUsersLoginTest(TestCase):
    def setUp(self):
        self.url = reverse('accounts:login')
        self.user = User.objects.create_user('foo', 'mail@example.com', 'bar', is_active=False)
        
    def test_post_login(self):
        data = {
            'username': self.user.username,
            'password': 'bar',  # Correct password
        }

        # Send post data to client.
        response = self.client.post(self.url, data)

        # Test that the redirect doesnot occur. Redirect occurs after successful login.
        # TODO: Test for `?next=` also.
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 302)
        error_message = "The email has not been verified. Please check your email\
        for verification link."
        self.assertFormError(response, 'form', None, error_message)
        # Test that the template isnot used. Because, it must be a redirection.
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'accounts/login.html')

        # Test that the user is not logged in.
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated())


class LogoutTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('hansolo', 'mailbox@postbox.box', 'princessleia')
        self.url = reverse('accounts:logout')
        self.client.login(username=self.user.username, password=self.user.password)
        self.response = self.client.get(self.url)

    def test_logout_user_is_deauthenticated(self):
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated())

    def test_logout_redirects_to_login_page(self):
        self.assertRedirects(self.response, expected_url=reverse('accounts:login'), status_code=302)