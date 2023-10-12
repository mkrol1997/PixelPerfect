from unittest import mock

from django.shortcuts import reverse
from django.test import TestCase, Client

from users.forms import UserRegisterForm
from users.models import User, Profile


class TestRegisterView(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')

    def test_should_return_true_when_user_registered(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@unittest.test',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }

        form = UserRegisterForm(form_data)
        self.assertTrue(form.is_valid())

        with mock.patch('os.mkdir', return_value=True):
            response = self.client.post(self.register_url, form_data)

        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed("users/login.html")
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_should_return_False_when_form_not_valid(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@unittest.test',
            'password1': 'testpassword',
            'password2': 'wrongpassword',
        }

        with mock.patch('os.mkdir', return_value=True):
            response = self.client.post(self.register_url, form_data)

        self.assertTemplateUsed("users/register.html")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='testuser').exists())


class TestProfileView(TestCase):
    def setUp(self) -> None:
        with mock.patch('os.mkdir', return_value=True):
            self.test_user = User.objects.create_user('testuser', 'testpassword')
        self.client = Client()
        self.profile_url = reverse('profile')

    def test_should_return_status_code_200_when_requested_profile_view(self):
        self.client.force_login(self.test_user)

        response = self.client.get(self.profile_url)

        self.assertTemplateUsed("users/profile.html")
        self.assertEqual(response.status_code, 200)

    def test_should_return_True_when_profile_updated(self):
        self.client.force_login(self.test_user)

        form_data = {
            'username': 'new_username',
            'email': 'test@email.test',
            'image': '',
        }

        test_profile = Profile.objects.filter(user=self.test_user)
        response = self.client.post(self.profile_url, form_data)

        self.assertTrue(test_profile.exists())
        self.assertTemplateUsed("users/contact.html")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.get(id=self.test_user.id).username, 'new_username')


class TestContactView(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.contact_url = reverse('contact')

    def test_should_return_status_code_200_when_request_contact_view(self):
        response = self.client.get(self.contact_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('users/contact.html')

    def test_should_return_status_code_302_when_contact_form_submitted(self):
        form_data = {
            'subject': "test_subject",
            'from_email': 'testuser@email.test',
            'recipient_list': 'test_receipent@contact.test',
            'message': 'test message',
        }

        with mock.patch('django.core.mail.send_mail', return_value=True):
            response = self.client.post(self.contact_url, form_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('users/contact.html')


class TestCustomLoginView(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        self.client = Client()
        self.login_url = reverse('login')

        with mock.patch('os.mkdir'):
            User.objects.create_user(**self.credentials)

    def test_should_return_response_status_code_200_when_request_login(self):
        response = self.client.get(self.login_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('users/login.html')

    def test_should_return_true_when_user_logged_in(self):
        response = self.client.post(self.login_url, self.credentials, follow=True)
        logged_user = response.context['user']

        self.assertTrue(logged_user.is_authenticated)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('pixel_perfect/dashboard.html')

    def test_should_return_true_when_not_logged_in_with_wrong_credentials(self):
        invalid_credentials = {
            'username': 'testuser',
            'password': 'invalid_password',
        }

        response = self.client.post(self.login_url, invalid_credentials, follow=True)
        logged_user = response.context['user']

        self.assertFalse(logged_user.is_authenticated)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('users/login.html')
