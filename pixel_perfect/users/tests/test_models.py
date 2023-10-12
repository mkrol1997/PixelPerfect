from django.test import TestCase
from users.models import Profile, User
from unittest import mock


class TestProfileModel(TestCase):
    def setUp(self):
        with mock.patch('os.mkdir', return_value=True):
            self.test_user = User.objects.create_user(username='Test', password='User')

    def test_should_return_true_when_profile_created(self):
        self.assertEqual(Profile.objects.filter(user=self.test_user).count(), 1)
