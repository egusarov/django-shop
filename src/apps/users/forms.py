from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "Input", "placeholder": "Value"}),
        label="Email",
    )

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "Input", "placeholder": "Value"}),
    )

    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={"class": "Input", "placeholder": "Value"}),
    )

    class Meta:
        model = User
        fields = ("email",)


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "Input", "placeholder": "Value"}),
        label="Email",
    )


class AccountInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["full_name", "phone", "email", "city", "address"]

        widgets = {
            "full_name": forms.TextInput(
                attrs={"class": "Input", "placeholder": "Value"}
            ),
            "phone": forms.TextInput(attrs={"class": "Input", "placeholder": "Value"}),
            "email": forms.EmailInput(
                attrs={"class": "Input", "placeholder": "example@mail.com"}
            ),
            "city": forms.TextInput(attrs={"class": "Input", "placeholder": "Value"}),
            "address": forms.Textarea(attrs={"class": "Textarea", "rows": 3}),
        }
