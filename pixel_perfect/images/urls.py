from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from images.views import (
    DeleteImageView,
    DownloadImageView,
    EnhanceImageView,
    FullEnhancementView,
    GoogleDriveUploadView,
    ImageGalleryView,
    UpscaleImageView,
    TrackTaskView,
)

urlpatterns = [
    path("upscale/", UpscaleImageView.as_view(), name="upscale"),
    path("enhance/", EnhanceImageView.as_view(), name="enhance"),
    path("full-enhancement/", FullEnhancementView.as_view(), name="full_enhancement"),
    path("list/", ImageGalleryView.as_view(), name="images_list"),
    path('track/', TrackTaskView.as_view()),
    path("download/<int:pk>", DownloadImageView.as_view(), name="save"),
    path("send-image/<int:pk>", GoogleDriveUploadView.as_view(), name="upload"),
    path("delete-image/", DeleteImageView.as_view(), name="delete_image"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
