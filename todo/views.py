from math import ceil

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
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

from todo.forms import TaskForm, TagForm, TaskSearchForm, TagSearchForm
from todo.mixins import (
    TagVerifyUrlDataMixin,
    TaskVerifyUrlDataMixin,
    FormKwargsMixin,
    FormValidMixin,
)
from todo.models import Tag, Task


@login_required
def index_view(request: HttpRequest) -> HttpResponse:
    tasks = Task.objects.filter(Q(user_id=request.user.id) & Q(status=True))
    finished_tasks_count = tasks.count()

    request.session["num_visits"] = request.session.get("num_visits", 0) + 1

    context = {
        "finished_tasks_count": finished_tasks_count,
        "num_visits": request.session["num_visits"],
    }

    return render(request, "todo/index.html", context=context)


def about_view(request: HttpRequest) -> HttpResponse:
    return render(request, "footer/about.html")


class TagListView(LoginRequiredMixin, generic.ListView):
    model = Tag
    paginate_by = 8

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = TagSearchForm(
            name=self.request.GET.get("name", "")
        )
        return context

    def get_queryset(self):
        queryset = Tag.objects.filter(user_id=self.request.user.id).order_by(
            "-created_at"
        )

        form = TaskSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])

        return queryset


class TagDetailView(
    LoginRequiredMixin, TagVerifyUrlDataMixin, generic.DetailView
):
    model = Tag


class TagCreateView(
    LoginRequiredMixin, FormKwargsMixin, FormValidMixin, generic.CreateView
):
    form_class = TagForm
    template_name = "todo/tag_form.html"

    def get_success_url(self):
        return f"{reverse('todo:tag-list')}?name={self.request.GET.get('name', '')}&page={self.request.GET.get('page', 1)}"


class TagUpdateView(
    LoginRequiredMixin,
    TagVerifyUrlDataMixin,
    FormKwargsMixin,
    generic.UpdateView,
):
    model = Tag
    form_class = TagForm

    def get_success_url(self):
        return f"{reverse('todo:tag-list')}?name={self.request.GET.get('name', '')}&page={self.request.GET.get('page', 1)}"


class TagDeleteView(
    LoginRequiredMixin, TagVerifyUrlDataMixin, generic.DeleteView
):
    model = Tag

    def get_success_url(self):
        page = int(self.request.GET["page"])
        count = int(self.request.GET["count"])
        per_page = int(self.request.GET["per_page"])

        count -= 1
        if ceil(count / per_page) < page:
            page = max(page - 1, 1)

        return f"{reverse('todo:tag-list')}?name={self.request.GET.get('name', '')}&page={page}"


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = TaskSearchForm(
            name=self.request.GET.get("name", "")
        )
        return context

    def get_queryset(self):
        queryset = Task.objects.filter(user_id=self.request.user.id).order_by(
            "-pinned", "-priority", "deadline"
        )

        form = TaskSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])

        return queryset


class TaskDetailView(
    LoginRequiredMixin, TaskVerifyUrlDataMixin, generic.DetailView
):
    model = Task


class TaskCreateView(
    LoginRequiredMixin, FormKwargsMixin, FormValidMixin, generic.CreateView
):
    form_class = TaskForm
    template_name = "todo/task_form.html"

    def get_success_url(self):
        return f"{reverse('todo:task-list')}?name={self.request.GET.get('name', '')}&page={self.request.GET['page']}"


class TaskUpdateView(
    LoginRequiredMixin,
    TaskVerifyUrlDataMixin,
    FormKwargsMixin,
    generic.UpdateView,
):
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        return f"{reverse('todo:task-list')}?name={self.request.GET.get('name', '')}&page={self.request.GET['page']}"


class TaskDeleteView(
    LoginRequiredMixin, TaskVerifyUrlDataMixin, generic.DeleteView
):
    model = Task

    def get_success_url(self):
        page = int(self.request.GET["page"])
        count = int(self.request.GET["count"])
        per_page = int(self.request.GET["per_page"])

        count -= 1
        if ceil(count / per_page) < page:
            page = max(page - 1, 1)

        return f"{reverse('todo:task-list')}?name={self.request.GET.get('name', '')}&page={page}"


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
