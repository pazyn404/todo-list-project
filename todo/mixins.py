from django.http import Http404
from django.shortcuts import get_object_or_404

from todo.models import Tag, Task


class TagVerifyUrlDataMixin:
    def get(self, request, *args, **kwargs):
        if get_object_or_404(Tag, pk=kwargs["pk"]).user_id != request.user.id:
            raise Http404()

        return super().get(request, *args, **kwargs)


class TaskVerifyUrlDataMixin:
    def get(self, request, *args, **kwargs):
        if get_object_or_404(Task, pk=kwargs["pk"]).user_id != request.user.id:
            raise Http404()

        return super().get(request, *args, **kwargs)


class FormKwargsMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class FormValidMixin:
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
