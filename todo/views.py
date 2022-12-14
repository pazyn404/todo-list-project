from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import (
    HttpResponseRedirect,
    HttpRequest,
    HttpResponse,
    Http404,
)
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from todo.forms import TaskForm, TagForm
from todo.functions import get_page_number_after_deletion
from todo.mixins import (
    TagVerifyUrlDataMixin,
    TaskVerifyUrlDataMixin,
    FormKwargsMixin,
    FormValidMixin,
)
from todo.models import Tag, Task


@login_required
def index_view(request: HttpRequest) -> HttpResponse:
    tasks_count = Task.objects.filter(user_id=request.user.id).count()
    finished_tasks_count = Task.objects.filter(Q(user_id=request.user.id) & Q(status=True)).count()

    request.session["num_visits"] = request.session.get("num_visits", 0) + 1

    context = {
        "tasks_count": tasks_count,
        "finished_tasks_count": finished_tasks_count,
        "num_visits": request.session["num_visits"],
        "test": "data",
    }

    return render(request, "todo/index.html", context=context)


def about_view(request: HttpRequest) -> HttpResponse:
    return render(request, "todo/about.html")


class TagListView(LoginRequiredMixin, generic.ListView):
    model = Tag
    paginate_by = 8

    def get_queryset(self):
        queryset = Tag.objects.filter(user_id=self.request.user.id).order_by(
            "-created_at"
        )

        name = self.request.GET.get("name")
        if name:
            return queryset.filter(name__icontains=name)

        return queryset


class TagDetailView(
    LoginRequiredMixin, TagVerifyUrlDataMixin, generic.DetailView
):
    model = Tag


class TagCreateView(
    LoginRequiredMixin, SuccessMessageMixin, FormKwargsMixin, FormValidMixin, generic.CreateView
):
    form_class = TagForm
    template_name = "todo/tag_form.html"
    success_message = "Tag was successfully created"

    def get_success_url(self):
        return f"{reverse('todo:tag-list')}?name={self.request.GET.get('name', '')}&page={self.request.GET.get('page', 1)}"


class TagUpdateView(
    LoginRequiredMixin,
    TagVerifyUrlDataMixin,
    SuccessMessageMixin,
    FormKwargsMixin,
    generic.UpdateView,
):
    model = Tag
    form_class = TagForm
    success_message = "Tag was successfully updated"

    def get_success_url(self):
        return f"{reverse('todo:tag-list')}?name={self.request.GET.get('name', '')}&page={self.request.GET.get('page', 1)}"


class TagDeleteView(
    LoginRequiredMixin, TagVerifyUrlDataMixin, generic.DeleteView
):
    model = Tag

    def get_success_url(self):
        page = int(self.request.GET.get("page", 1))
        count = int(self.request.GET.get("count", 1))
        per_page = int(self.request.GET.get("per_page", 1))

        new_page = get_page_number_after_deletion(page, count, per_page)

        messages.add_message(self.request, messages.SUCCESS, "Tag was successfully deleted")
        return f"{reverse('todo:tag-list')}?name={self.request.GET.get('name', '')}&page={new_page}"


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 4

    def get_queryset(self):
        queryset = Task.objects.filter(user_id=self.request.user.id).order_by(
            "-pinned", "-priority", "deadline"
        )

        name = self.request.GET.get("name")
        if name:
            return queryset.filter(name__icontains=name)

        return queryset


class TaskDetailView(
    LoginRequiredMixin, TaskVerifyUrlDataMixin, generic.DetailView
):
    model = Task


class TaskCreateView(
    LoginRequiredMixin, SuccessMessageMixin, FormKwargsMixin, FormValidMixin, generic.CreateView
):
    form_class = TaskForm
    template_name = "todo/task_form.html"
    success_message = "Task was successfully created"

    def get_success_url(self):
        return f"{reverse('todo:task-list')}?name={self.request.GET.get('name', '')}&page={self.request.GET['page']}"


class TaskUpdateView(
    LoginRequiredMixin,
    TaskVerifyUrlDataMixin,
    SuccessMessageMixin,
    FormKwargsMixin,
    generic.UpdateView,
):
    model = Task
    form_class = TaskForm
    success_message = "Task was successfully updated"

    def get_success_url(self):
        return f"{reverse('todo:task-list')}?name={self.request.GET.get('name', '')}&page={self.request.GET['page']}"


class TaskDeleteView(
    LoginRequiredMixin, TaskVerifyUrlDataMixin, generic.DeleteView
):
    model = Task

    def get_success_url(self):
        page = int(self.request.GET.get("page", 1))
        count = int(self.request.GET.get("count", 1))
        per_page = int(self.request.GET.get("per_page", 1))

        new_page = get_page_number_after_deletion(page, count, per_page)

        messages.add_message(self.request, messages.SUCCESS, "Task was successfully deleted")
        return f"{reverse('todo:task-list')}?name={self.request.GET.get('name', '')}&page={new_page}"


def change_status_view(request, pk: int):
    task = get_object_or_404(Task, pk=pk)

    if task.user_id != request.user.id:
        raise Http404()

    task.status = not task.status
    task.save()

    return HttpResponseRedirect(
        f"{reverse('todo:task-list')}?name={request.GET.get('name', '')}&page={request.GET.get('page', 1)}"
    )


def switch_pinned_view(request, pk: int):
    task = get_object_or_404(Task, pk=pk)

    if task.user_id != request.user.id:
        raise Http404()

    task.pinned = not task.pinned
    task.save()

    return HttpResponseRedirect(
        f"{reverse('todo:task-list')}?name={request.GET.get('name', '')}&page={request.GET.get('page', 1)}"
    )
