from django.urls import path
from django.contrib.auth.views import LoginView
from accounts.forms import CustomLoginForm
from accounts.views import signup
from .views import ResetPasswordView
from django.contrib.auth import views as auth_views

app_name = "hotel"
urlpatterns = [
    path(
        "login/", LoginView.as_view(authentication_form=CustomLoginForm), name="login"
    ),
    path(
        "signup/",
        signup,
        name="signup",
    ),
    path("password_reset/", ResetPasswordView.as_view(), name="password_reset"),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
