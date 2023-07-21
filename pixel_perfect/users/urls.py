from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import TemplateView
from .views import (
    ProfileView,
    UserRegisterView,
    OAuth2GoogleDriveAccessView,
    OAuth2GoogleDriveAccessCallbackView,
    ImageUploadView,
    RedirectInvalidLoginView,
)


urlpatterns = [
    path('', LoginView.as_view(
        template_name='users/login.html',
        redirect_authenticated_user=True),
         name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('authorize/', OAuth2GoogleDriveAccessView.as_view(), name='authorize'),
    path('oauth2callback/', OAuth2GoogleDriveAccessCallbackView.as_view(), name='callback'),
    path('send-image/', ImageUploadView.as_view(), name='upload'),
    path('accounts/social/signup/', RedirectInvalidLoginView.as_view(), name='signup_redirect'),
    path('dashboard/', TemplateView.as_view(template_name='users/confirm.html'))
]
