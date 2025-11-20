from django.urls import path
from .views import register, login_view, account, logout_view

app_name = "users"

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("account/", account, name="account"),
]
