from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import PasswordChangeView
from django.urls import include, path

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("", include("users.urls")),
        path(
            "accounts/password/change/",
            PasswordChangeView.as_view(template_name="users/change_password.html"),
            name="account_change_password",
        ),
        path("accounts/", include("allauth.urls")),
        path("images/", include("images.urls")),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
