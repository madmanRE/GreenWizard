from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from .models import Profile
from .forms import RegisterForm, ProfileForm, PasswordRecovery
from django.http import HttpResponseRedirect, HttpResponse
from django.views import View
from django.db import IntegrityError
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from django.core.mail import send_mail
from django.conf import settings


class PasswordRecoveryView(View):
    def get(self, request):
        form = PasswordRecovery
        return render(request, "profile_app/password_recovery.html", {"form": form})

    def post(self, request):
        form = PasswordRecovery(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            name = cd["username"]
            email = cd["email"]
            profile = Profile.objects.get(username=name, email=email)
            password = profile.password
            send_mail(
                f"Восстановление пароля GreenWizard",
                "",
                settings.EMAIL_HOST_USER,
                [email],
                html_message=f'<p>Уважаемый <strong>{name}</strong>, больше не теряйте ваш пароль - '
                             f'<strong style="color:green">{password}</strong>. '
                             f'Посмотрите новые товары в <a href="http://127.0.0.1:8000/">нашем магазине!</a></p>',
            )
            return redirect("/")
        return render(request, "profile_app/password_recovery.html", {"form": form})


class RegisterView(View):
    def get(self, request):
        form = RegisterForm
        return render(request, "profile_app/register.html", {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                user = User.objects.create_user(username=username)
                user.set_password(password)
                user.backend = (
                    ModelBackend().__class__.__module__
                    + "."
                    + ModelBackend().__class__.__name__
                )
                user.save()
                login(request, user)
                profile = Profile.objects.create(
                    user=user,
                    username=username,
                    password=password,
                    phone=form.cleaned_data["phone"],
                    email=form.cleaned_data["email"],
                )
                profile.save()
                return redirect("/")
            except IntegrityError:
                form.add_error("login", "Пользователь с таким логином уже существует")

        return render(request, "profile_app/register.html", {"form": form})


class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileForm
    success_url = "/"


class ProfileView(DetailView):
    template_name = "profile_app/profile.html"
    model = Profile
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object
        context["profile"] = profile
        return context
