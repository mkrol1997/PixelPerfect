from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import ClearableFileInput
from django.utils.safestring import mark_safe
from users.models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        for fieldname in ["username", "email", "password1", "password2"]:
            self.fields[fieldname].help_text = None

    def clean(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                mark_safe(
                    f"An account with email address {email} already exists. <br>"
                    f"Please login using this email or choose different email address."
                )
            )
        return self.cleaned_data


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields["email"].required = True


class MyClearableFileInput(ClearableFileInput):
    initial_text = ""
    input_text = ""


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image"]
        widgets = {"image": MyClearableFileInput}


class ContactForm(forms.Form):
    name = forms.CharField(required=True, max_length=50, widget=forms.TextInput(attrs={"placeholder": "Name"}))
    email = forms.EmailField(
        required=True, label="Email Address", widget=forms.EmailInput(attrs={"placeholder": "Email"})
    )
    subject = forms.ChoiceField(
        choices=[
            ("General", "General"),
            ("Support", "Technical Support"),
            ("Bug Report", "Bug Report"),
            ("Feedback", "Feedback"),
            ("Suggestion", "Suggestions"),
        ]
    )
    message = forms.CharField(required=True, widget=forms.Textarea(attrs={"placeholder": "Write your message here"}))
