from django.urls import path

from todo.views import (
    index_view,
    TagListView,
    TagCreateView,
    TagUpdateView,
    TagDeleteView,
    TagDetailView,
    TaskListView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    TaskDetailView,
    change_status_view,
    switch_pinned_view,
)

urlpatterns = [
    path("", index_view, name="index"),
    path("tags/", TagListView.as_view(), name="tag-list"),
    path("tags/<int:pk>/", TagDetailView.as_view(), name="tag-detail"),
    path("tags/create/", TagCreateView.as_view(), name="tag-create"),
    path("tags/<int:pk>/update/", TagUpdateView.as_view(), name="tag-update"),
    path("tags/<int:pk>/delete/", TagDeleteView.as_view(), name="tag-delete"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path(
        "tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"
    ),
    path(
        "tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"
    ),
    path(
        "tasks/<int:pk>/change_status/",
        change_status_view,
        name="task-change-status",
    ),
    path(
        "tasks/<int:pk>/switch_pinned/",
        switch_pinned_view,
        name="task-switch-pinned",
    ),
]

app_name = "todo"
