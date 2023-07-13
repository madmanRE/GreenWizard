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


class PasswordRecoveryView(View):
    def get(self, request):
        form = PasswordRecovery
        return render(request, 'profile_app/password_recovery.html', {'form': form})

    def post(self, request):
        pass

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
