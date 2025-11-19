from django.urls import path
from .views import register, login_view, account

app_name = "users"

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("account/", account, name="account"),
]
