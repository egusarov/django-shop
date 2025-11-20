from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, AccountInfoForm
from ..orders.models import Order


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("home")
    else:
        form = LoginForm()

    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def account(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by("-created_at")

    if request.method == "POST":
        form = AccountInfoForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("users:account")
    else:
        form = AccountInfoForm(instance=user)

    return render(request, "users/account.html", {"form": form, "orders": orders})
