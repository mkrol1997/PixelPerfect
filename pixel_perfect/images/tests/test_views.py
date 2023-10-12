from unittest import mock

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from images.models import EnhancedImages


class TestUpscaleImageView(TestCase):
    def setUp(self) -> None:
        with mock.patch('os.mkdir', return_value=True):
            self.test_user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.upscale_img_url = reverse('upscale')

    def test_should_return_status_code_200_when_requested_upscale_image_view(self):
        response = self.client.get(self.upscale_img_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('images/upscale-image.html')


class TestDeleteImageView(TestCase):
    def setUp(self):
        with mock.patch('os.mkdir', return_value=True):
            self.test_user = User.objects.create_user(username='testuser', password='testpassword')

        self.test_image = EnhancedImages.objects.create(
            img_name='test_img.jpg',
            img_owner=self.test_user,
            img_path='media/test_img.jpg'
        )
        self.success_message = "Image has been deleted successfully."
        self.client.login(username='testuser', password='testpassword')
        self.delete_img_url = reverse('delete_image')

    def test_should_return_status_code_200_when_requested_image_deleted_successfully(self):
        self.assertEqual(EnhancedImages.objects.all().count(), 1)

        response = self.client.post(self.delete_img_url + '?img_id=' + str(self.test_image.id), follow=True)

        self.assertEqual(EnhancedImages.objects.all().count(), 0)
        self.assertRedirects(response, reverse('images_list'))
        self.assertTemplateUsed('images/images-list.html')
        self.assertContains(response, self.success_message)


class TestImageGalleryView(TestCase):
    def setUp(self):
        with mock.patch('os.mkdir', return_value=True):
            self.test_user = User.objects.create_user(username='testuser', password='testpassword')

        self.client.login(username='testuser', password='testpassword')
        self.gallery_url = reverse('images_list')

        self.images_queryset = [EnhancedImages.objects.create(
            img_name=f'test_img_{index}.jpg',
            img_owner=self.test_user,
            img_path=f'media/test_img_{index}.jpg') for index in range(1, 8)]

    def test_image_gallery_view(self):
        response = self.client.get(self.gallery_url)
        images_context = response.context['images']

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'images/images-list.html')
        self.assertEqual(images_context.count(), 6)

        [self.assertIn(image_object, images_context) for image_object in self.images_queryset[:-1]]
        self.assertNotIn(self.images_queryset[-1], images_context)


class TestDownloadImageView(TestCase):
    def setUp(self):
        with mock.patch('os.mkdir', return_value=True):
            self.test_user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.image = EnhancedImages.objects.create(
            img_name='Test Image',
            img_owner=self.test_user,
            img_path='path/to/mocked_image.jpg')

    @mock.patch('builtins.open', new_callable=mock.mock_open, read_data=b'mocked_image.jpg')
    def test_should_return_true_when_response_served_image_file_on_request(self, mock_handler):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('save', args=[self.image.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/octet-stream')
