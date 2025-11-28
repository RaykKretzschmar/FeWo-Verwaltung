from django.urls import path
from .views import SignUpView, profile_settings, subscription_view, cancel_subscription

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("settings/", profile_settings, name="profile_settings"),
    path("subscription/", subscription_view, name="subscription"),
    path("subscription/cancel/", cancel_subscription, name="cancel_subscription"),
]
