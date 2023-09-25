from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings


class CustomLoginRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request, messages.INFO, settings.PERMISSION_DENIED_MESSAGE)
            return self.handle_no_permission()
        return super(CustomLoginRequiredMixin, self).dispatch(request, *args, **kwargs)
