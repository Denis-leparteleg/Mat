from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    error_messages = {
    'password_mismatch': ("The two password fields didn't match."),
}
    password1 = forms.CharField(
    label=("Password"),
    strip=False,
    widget=forms.PasswordInput,
)
    password2 = forms.CharField(
    label=("Password confirmation"),
    widget=forms.PasswordInput,
    strip=False,
)

    class Meta:
        model = User
        fields = ("username", "password1","password2")
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
        }
