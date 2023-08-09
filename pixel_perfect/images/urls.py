from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from images.views import (
    EnhanceImageView,
    ImageSaveView,
    ImagesListView,
    ImageUploadView,
    UpscaleImageView,
)

urlpatterns = [
    path("upscale/", UpscaleImageView.as_view(), name="upscale"),
    path("enhance/", EnhanceImageView.as_view(), name="enhance"),
    path("list/", ImagesListView.as_view(), name="images-list"),
    path("send-image/<int:pk>", ImageUploadView.as_view(), name="upload"),
    path("download/<int:pk>", ImageSaveView.as_view(), name="save"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
