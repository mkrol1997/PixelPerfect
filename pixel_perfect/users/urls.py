from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import (
    LogoutView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
    PasswordChangeView,
    TemplateView,
)

from django.urls import path
from users.views import (
    ContactView,
    CustomLoginView,
    DeleteUserView,
    OAuth2GoogleDriveAccessCallbackView,
    OAuth2GoogleDriveAccessView,
    ProfileView,
    RedirectInvalidLoginView,
    UserRegisterView,
    PasswordChangeDoneCustomView,
)

urlpatterns = [
    path("", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("delete/profile/", DeleteUserView.as_view(), name="delete_profile"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("authorize/", OAuth2GoogleDriveAccessView.as_view(), name="authorize"),
    path("oauth2callback/", OAuth2GoogleDriveAccessCallbackView.as_view(), name="callback"),
    path("accounts/social/signup/", RedirectInvalidLoginView.as_view(), name="signup_redirect"),
    path("dashboard/", TemplateView.as_view(template_name="pixel_perfect/dashboard.html"), name="dashboard"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("password_reset/",
         PasswordResetView.as_view(template_name="users/registration/password_reset.html"),
         name="password_reset"),
    path("password_reset/done",
         PasswordResetDoneView.as_view(template_name="users/registration/password_reset_done.html"),
         name="password_reset_done"),
    path("password_reset/<uidb64>/<token>",
         PasswordResetConfirmView.as_view(template_name="users/registration/password_reset_confirm.html"),
         name="password_reset_confirm"),
    path("password_reset/complete",
         PasswordResetCompleteView.as_view(template_name="users/registration/password_reset_complete.html"),
         name="password_reset_complete"),
    path("accounts/password/change/",
         PasswordChangeView.as_view(template_name="users/change_password.html"),
         name="account_change_password"),
    path("accounts/password/change/done",
         PasswordChangeDoneCustomView.as_view(),
         name="password_change_done")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
