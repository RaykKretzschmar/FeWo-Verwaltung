from django.urls import path
from .views import SignUpView, profile_settings

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("settings/", profile_settings, name="profile_settings"),
]
