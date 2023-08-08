from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView, TemplateView
from django.urls import path
from users.views import (
    ImageSaveView,
    ImageUploadView,
    OAuth2GoogleDriveAccessCallbackView,
    OAuth2GoogleDriveAccessView,
    ProfileView,
    RedirectInvalidLoginView,
    UserRegisterView,
)

urlpatterns = [
    path("", LoginView.as_view(template_name="users/login.html", redirect_authenticated_user=True), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("authorize/", OAuth2GoogleDriveAccessView.as_view(), name="authorize"),
    path("oauth2callback/", OAuth2GoogleDriveAccessCallbackView.as_view(), name="callback"),
    path("send-image/<int:pk>", ImageUploadView.as_view(), name="upload"),
    path("accounts/social/signup/", RedirectInvalidLoginView.as_view(), name="signup_redirect"),
    path("dashboard/", TemplateView.as_view(template_name="users/dashboard.html"), name="dashboard"),
    path("download/<int:pk>", ImageSaveView.as_view(), name="save"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
