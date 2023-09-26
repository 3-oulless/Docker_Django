from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View
from .forms import LoginForm, CreateUserForm
from .models import User


def login_user(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                phone=form.cleaned_data.get("phone"),
                password=form.cleaned_data.get("password"),
            )

            if user is not None:
                login(request, user)
                return redirect("post:post-list")

    context = {"form": form}
    return render(request, "Account/login.html", context)


class CreateUser(View):
    def get(self, request):
        form = CreateUserForm()
        context = {"form": form}
        return render(request, "Account/create.html", context)

    def post(self, request):
        form = CreateUserForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                phone = form.cleaned_data.get("phone")
                email = form.cleaned_data.get("email")
                password = form.cleaned_data.get("password")

                User.objects.create_user(
                    phone=phone, email=email, password=password
                )

                return redirect("account:login")
        context = {"form": form}
        return render(request, "Account/create.html", context)
