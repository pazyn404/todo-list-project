from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic

from registration.forms import UserCreateForm
from registration.mixins import UserVerifyUrlDataMixin
from registration.models import User


class UserCreateView(SuccessMessageMixin, generic.CreateView):
    model = User
    form_class = UserCreateForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("registration:login")
    success_message = "Account was successfully created"


class UserUpdateView(
    LoginRequiredMixin, UserVerifyUrlDataMixin, SuccessMessageMixin, generic.UpdateView
):
    model = User
    fields = ["username", "first_name", "last_name"]
    template_name = "registration/update.html"
    success_url = reverse_lazy("todo:index")

    def get_success_message(self, cleaned_data):
        user = self.request.user
        user_data = {
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }

        if user_data != cleaned_data:
            return "Personal information was successfully updated"


class UserDeleteView(
    LoginRequiredMixin, UserVerifyUrlDataMixin, generic.DeleteView
):
    model = User
    success_url = reverse_lazy("registration:login")


@login_required
def user_confirm_deletion_view(request, *args, **kwargs):
    if request.user.pk != kwargs["pk"]:
        raise Http404()

    if not request.POST["password"]:
        return render(
            request,
            "registration/user_confirm_delete.html",
            {"password_error": "Empty password"},
        )

    if not request.user.check_password(request.POST["password"]):
        return render(
            request,
            "registration/user_confirm_delete.html",
            {"password_error": "Incorrect password"},
        )

    request.user.delete()
    messages.add_message(request, messages.SUCCESS, "Account was successfully deleted")
    return HttpResponseRedirect(reverse("registration:login"))
