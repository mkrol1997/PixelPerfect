from __future__ import annotations

import google.auth
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import reverse, redirect
from django.views import View
from django.views.generic import CreateView
from django.views.generic.base import RedirectView
from users.forms import UserRegisterForm
from users.gdrive.manager import get_gdrive_folder_id, uploadImage


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_joined'] = self.request.user.date_joined.strftime('%m/%d/%Y')
        return context


class RedirectInvalidLoginView(RedirectView):
    url = 'http://localhost:8000'

    def get_redirect_url(self, *args, **kwargs):
        messages.error(self.request, 'User with this email already exist. Please log in with email and password.')
        return super().get_redirect_url(*args, **kwargs)


class UserRegisterView(SuccessMessageMixin, CreateView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_message = "Your profile was created successfully"

    def get_success_url(self):
        return reverse('login')


class OAuth2GoogleDriveAccessView(View):
    def get(self, request):
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            'client_secret.json',
            scopes=['https://www.googleapis.com/auth/drive']
        )

        flow.redirect_uri = settings.GOOGLE_OAUTH_REDIRECT_URI

        authorization_url, state = flow.authorization_url(
            access_type='online',
            login_hint=request.user.email,
            include_granted_scopes='false')

        request.session['state'] = state

        return redirect(authorization_url)


class OAuth2GoogleDriveAccessCallbackView(View):
    def get(self, request):
        state = request.session['state']
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            'client_secret.json',
            scopes=['https://www.googleapis.com/auth/drive'],
            state=state)

        flow.redirect_uri = settings.GOOGLE_OAUTH_REDIRECT_URI

        # from django.conf import settings

        authorization_response = request.build_absolute_uri()

        flow.fetch_token(authorization_response=authorization_response)

        credentials = flow.credentials

        print(credentials)

        request.session['credentials'] = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }

        return redirect(reverse('profile'))


class ImageUploadView(View):
    def get(self, request):
        if not request.session.get('credentials', False):
            return redirect('authorize')

        credentials = google.oauth2.credentials.Credentials(
            **request.session['credentials'])

        folder_id = get_gdrive_folder_id(credentials)

        uploadImage(credentials, '26534.jpg', 'image-1.jpg', 'image/jpeg', folder_id)

        return redirect('profile')
