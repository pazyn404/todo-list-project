from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic

from registration.forms import UserCreateForm
from registration.models import User


class UserCreateView(generic.CreateView):
    model = User
    form_class = UserCreateForm
    success_url = reverse_lazy("registration:login")
    template_name = "registration/register.html"


class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    fields = ["username", "first_name", "last_name"]
    success_url = reverse_lazy("todo:index")
    template_name = "registration/update.html"

    def get(self, request, *args, **kwargs):
        if request.user.pk != kwargs["pk"]:
            raise Http404()
        return super().get(request, *args, **kwargs)


class UserDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = User
    success_url = reverse_lazy("registration:login")
    extra_context = {
        "successful_deletion_message": "Account was successfully deleted"
    }

    def get(self, request, *args, **kwargs):
        if request.user.pk != kwargs["pk"]:
            raise Http404()

        return super().get(request, *args, **kwargs)


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
    return HttpResponseRedirect(reverse("registration:login"))
