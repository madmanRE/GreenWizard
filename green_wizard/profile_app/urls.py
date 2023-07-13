from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import RegisterView, ProfileUpdateView, ProfileView, PasswordRecoveryView
from django.conf import settings
from django.conf.urls.static import static

app_name = "profile_app"

urlpatterns = (
    [
        path(
            "password_recovery/",
            PasswordRecoveryView.as_view(),
            name="password_recovery",
        ),
        path(
            "login/",
            LoginView.as_view(template_name="profile_app/login.html"),
            name="login",
        ),
        path("logout/", LogoutView.as_view(next_page="catalog:index"), name="logout"),
        path("register/", RegisterView.as_view(), name="register"),
        path(
            "profile/<int:pk>/update/",
            ProfileUpdateView.as_view(),
            name="profile_update",
        ),
        path("profile/<int:pk>/", ProfileView.as_view(), name="profile_view"),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
