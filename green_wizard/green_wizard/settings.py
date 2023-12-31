"""
Django settings for green_wizard project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-&%-&e%_oq1_3ia@#z1&qs3co29-jfl^y$-e=8w1dx%!(p(4401"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "0.0.0.0",
    "127.0.0.1",
    "localhost",
]
INTERNAL_IPS = [
    "127.0.0.1",

]

SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "catalog.apps.CatalogConfig",
    "profile_app.apps.ProfileAppConfig",
    "blog.apps.BlogConfig",
    "cart.apps.CartConfig",
    "orders.apps.OrdersConfig",
    "payment.apps.PaymentConfig",
    "django.contrib.postgres",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "bootstrap5",
    "taggit",
    "social_django",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "green_wizard.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "catalog.context_processors.categories",
                "catalog.context_processors.most_popular_games",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
                "cart.context_processors.cart",
            ],
        },
    },
]

WSGI_APPLICATION = "green_wizard.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR / 'db.sqlite3'),
#     }
# }


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "greenwizard",
        "USER": "greenwizard",
        "PASSWORD": "admin",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "profile_app:login"
LOGOUT_URL = "profile_app:logout"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "social_core.backends.google.GoogleOAuth2",
    "social_core.backends.vk.VKOAuth2",
    "social_core.backends.github.GithubOAuth2",
]

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = (
    "279112470741-d2no0lv8m21oa3h240b8637bfgbmbdva.apps.googleusercontent.com"
)
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "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"

SOCIAL_AUTH_VK_OAUTH2_KEY = "51689741"
SOCIAL_AUTH_VK_OAUTH2_SECRET = "YoRs0BVO2ZtlLCzjvHDQ"

SOCIAL_AUTH_GITHUB_KEY = "057599a02c935f6ea756"
SOCIAL_AUTH_GITHUB_SECRET = "742236f6462b195c523a9bf605a9a084df645f9a"

EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "romangvaramadze@gmail.com"
EMAIL_HOST_PASSWORD = "xnvgkiswgzoezxcj"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

CART_SESSION_ID = "cart"

STRIPE_PUBLISHABLE_KEY = "pk_test_51NPNkRJbl0LlWzfnqOVTzixWbRuQIbD0O3EVSwOYLAz9dVRZHOMJFXAokPIc0lONxMtGxFlslATJn6EfDaOa1QTl00n9JeM00Q"
STRIPE_SECRET_KEY = "sk_test_51NPNkRJbl0LlWzfnBCWu8NTfJk9R2xIEGbQxacxYHzSAV113JhRCRmS9wytv2GqhdkTLCJx0ZyaLkuVQJ5nUIoGl00rt5s4zR1"
STRIPE_API_VERSION = "2022-08-01"
STRIPE_WEBHOOK_SECRET = (
    "whsec_4bb1bbe8fd3d379776db5603c48cfdb56851166a7c1a779843207991a2717dcb"
)
