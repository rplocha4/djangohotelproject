from django.urls import path
from django.contrib.auth.views import LoginView
from accounts.forms import CustomLoginForm
from accounts.views import signup, dashboard

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
    path(
        "dashboard/",
        dashboard,
        name="dashboard",
    ),
]
