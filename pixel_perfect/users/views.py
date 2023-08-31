from __future__ import annotations

import google_auth_oauthlib
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.views.generic.base import RedirectView
from django.views.generic.edit import DeleteView, FormView
from users.forms import ContactForm, ProfileUpdateForm, UserRegisterForm, UserUpdateForm


class DeleteUserView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    success_url = reverse_lazy("login")
    success_message = "Your account has been deleted."

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.request.user.pk)

    def delete(self, request, *args, **kwargs):
        messages.info(self.request, self.success_message)
        return super(DeleteUserView, self).delete(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, pk=self.request.user.pk)
        context["date_joined"] = self.request.user.date_joined.strftime("%m/%d/%Y")
        context["user_form"] = UserUpdateForm(instance=user)
        context["profile_form"] = ProfileUpdateForm(instance=user.profile)
        return context

    def post(self, request, *args, **kwargs):
        user_form = UserUpdateForm(instance=request.user, data=self.request.POST)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect("profile")

        messages.error(request, "Something gone wrong. Try again!")
        return redirect("profile")


class RedirectInvalidLoginView(RedirectView):
    url = "http://localhost:8000"

    def get_redirect_url(self, *args, **kwargs):
        messages.error(self.request, "User with this email already exist. Please log in with email and password.")
        return super().get_redirect_url(*args, **kwargs)


class UserRegisterView(SuccessMessageMixin, CreateView):
    template_name = "users/registration/register.html"
    form_class = UserRegisterForm
    success_message = "Your profile was created successfully"

    def get_success_url(self):
        return reverse("login")


class OAuth2GoogleDriveAccessView(View):
    def get(self, request):
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            "client_secret.json", scopes=["https://www.googleapis.com/auth/drive.file"]
        )

        flow.redirect_uri = settings.GOOGLE_OAUTH_REDIRECT_URI

        authorization_url, state = flow.authorization_url(
            access_type="online", login_hint=request.user.email, include_granted_scopes="false"
        )

        request.session["state"] = state

        return redirect(authorization_url)


class OAuth2GoogleDriveAccessCallbackView(View):
    def get(self, request):
        state = request.session["state"]
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            "../client_secret.json", scopes=["https://www.googleapis.com/auth/drive.file"], state=state
        )

        flow.redirect_uri = settings.GOOGLE_OAUTH_REDIRECT_URI

        authorization_response = request.build_absolute_uri()

        flow.fetch_token(authorization_response=authorization_response)

        credentials = flow.credentials

        request.session["credentials"] = {
            "token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "token_uri": credentials.token_uri,
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "scopes": credentials.scopes,
        }

        return redirect(reverse("upload", kwargs={"pk": request.session.get("img_id")}))


class ContactView(FormView):
    template_name = "users/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact")
    success_message = "Thank you for your feedback! Message sent successfully"

    def form_valid(self, form):
        send_mail(
            subject=form.cleaned_data.get("subject"),
            from_email=None,
            recipient_list=["emailziutka1@gmail.com"],
            message=f'From: {form.cleaned_data.get("email")}\nMessage: {form.cleaned_data.get("message")}',
        )
        return super(ContactView, self).form_valid(form)
