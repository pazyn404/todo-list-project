from django.urls import path

from todo.views import (
    TagListView,
    TaskListView,
    TagCreateView,
    TagUpdateView,
    TagDeleteView,
    TaskCreateView,
    TaskDeleteView,
    TaskUpdateView,
    change_status_view,
    TaskDetailView,
    index_view, SchedulerUpdateView,
)

urlpatterns = [
    path("", index_view, name="index"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>", TaskDetailView.as_view(), name="task-detail"),
    path("tags/", TagListView.as_view(), name="tag-list"),
    path("tags/create", TagCreateView.as_view(), name="tag-create"),
    path("tags/<int:pk>/update", TagUpdateView.as_view(), name="tag-update"),
    path("tags/<int:pk>/delete", TagDeleteView.as_view(), name="tag-delete"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path(
        "tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"
    ),
    path(
        "tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"
    ),
    path(
        "scheduler/<int:pk>/update/", SchedulerUpdateView.as_view(), name="scheduler-update"
    ),
    path(
        "tasks/<int:pk>/change_status/",
        change_status_view,
        name="task-change-status",
    ),
]

app_name = "todo"
