from unittest import mock

from django.contrib.auth.models import User
from django.test import TestCase

from images.models import EnhancedImages


class TestEnhancedImagesModel(TestCase):
    def setUp(self):
        with mock.patch('os.mkdir', return_value=True):
            self.test_user = User.objects.create_user(username='testuser', password='testpassword')

    def test_should_return_true_when_enhanced_image_created(self):
        enhanced_image = EnhancedImages.objects.create(
            img_name='test_image.jpg',
            img_owner=self.test_user,
            img_path='media/profile_pics/default.png'
        )

        self.assertEqual(EnhancedImages.objects.filter(img_name='test_image.jpg').count(), 1)
        self.assertEqual(enhanced_image.img_name, 'test_image.jpg')
        self.assertEqual(enhanced_image.img_owner, self.test_user)
        self.assertIsNotNone(enhanced_image.date_created)
        self.assertEqual(enhanced_image.img_path, 'media/profile_pics/default.png')
