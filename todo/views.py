from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic

from todo.forms import TaskForm
from todo.models import Tag, Task, Scheduler

@login_required
def index_view(request: HttpRequest) -> HttpResponse:
    finished_tasks_count = Count("Task", filter=Q(task__schedulers=request.user) & Q(status=True))
    not_finished_tasks_count = Count("Task", filter=Q(task__schedulers=request.user) & Q(status=False))

    context = {
        "finished_tasks_count": finished_tasks_count,
        "not_finished_tasks_count": not_finished_tasks_count,
    }

    return render(request, "todo/index.html", context=context)


class TagListView(LoginRequiredMixin, generic.ListView):
    model = Tag
    paginate_by = 5
    queryset = Tag.objects.all()


class TagCreateView(LoginRequiredMixin, generic.CreateView):
    model = Tag
    fields = "__all__"
    success_url = reverse_lazy("todo:tag-list")


class TagUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Tag
    fields = "__all__"
    success_url = reverse_lazy("todo:tag-list")


class TagDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Tag
    success_url = reverse_lazy("todo:tag-list")


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 4
    queryset = Task.objects.prefetch_related("tags")


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    queryset = Task.objects.prefetch_related("tags")


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("todo:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("todo:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("todo:task-list")


class SchedulerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Scheduler
    fields = "__all__"
    success_url = reverse_lazy("todo:index")


@login_required
def change_status_view(request: HttpRequest, pk: int) -> HttpResponseRedirect:
    task = Task.objects.get(pk=pk)
    task.status = not task.status
    task.save()

    return HttpResponseRedirect(reverse("todo:task-list"))
