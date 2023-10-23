from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("", include("users.urls")),
        path("images/", include("images.urls")),
        path("accounts/", include("allauth.urls")),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

handler404 = 'pixel_perfect.handlers.Custom404Handler'
handler500 = 'pixel_perfect.handlers.Custom500Handler'

