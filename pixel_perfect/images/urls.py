from django.urls import path

from images.views import UpscaleImageView

urlpatterns = [
    path('upscale/', UpscaleImageView.as_view(), name='upscale'),
]
