from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from images.views import EnhanceImageView, ImagesListView, UpscaleImageView

urlpatterns = [
    path("upscale/", UpscaleImageView.as_view(), name="upscale"),
    path("enhance/", EnhanceImageView.as_view(), name="enhance"),
    path("list/", ImagesListView.as_view(), name="images-list"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
