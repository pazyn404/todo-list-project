from django.urls import path, include
from django.views.generic import TemplateView

from registration.views import (
    UserCreateView,
    UserUpdateView,
    UserDeleteView,
    user_confirm_deletion_view,
)

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("register/", UserCreateView.as_view(), name="register"),
    path("<int:pk>/update/", UserUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", UserDeleteView.as_view(), name="delete"),
    path(
        "<int:pk>/confirm_deletion/",
        user_confirm_deletion_view,
        name="confirm-deletion",
    ),
    path(
        "settings/",
        TemplateView.as_view(template_name="registration/settings.html"),
        name="settings",
    ),
]

app_name = "registration"
