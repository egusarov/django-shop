from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "Input", "placeholder": "Value"}),
        label="Email"
    )

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "Input", "placeholder": "Value"})
    )

    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={"class": "Input", "placeholder": "Value"})
    )

    class Meta:
        model = User
        fields = ("email",)


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "Input", "placeholder": "Value"}),
        label="Email"
    )
