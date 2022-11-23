from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

from pytz import timezone

from todo_list import settings


class Tag(models.Model):
    user = models.ForeignKey(
        "registration.User",
        related_name="tags",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=63)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user_id", "name"], name="name_user_unique"
            ),
        ]

    def __str__(self) -> str:
        return self.name


class Task(models.Model):
    STATUS_CHOICES = (
        (True, "Done"),
        (False, "Not done"),
    )

    PRIORITY_CHOICES = (
        (1, "Highest"),
        (2, "Critical"),
        (3, "Alarming"),
        (4, "Act soon"),
        (5, "Low"),
    )
    user = models.ForeignKey(
        "registration.User", related_name="tasks", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    status = models.BooleanField(default=False, choices=STATUS_CHOICES)
    priority = models.IntegerField(default=3, choices=PRIORITY_CHOICES)
    pinned = models.BooleanField(default=False)
    tags = models.ManyToManyField("Tag", related_name="tasks")

    @property
    def status_display_name(self) -> str:
        for status_code, status_display_name in Task.STATUS_CHOICES:
            if status_code == self.status:
                return status_display_name

    @property
    def priority_display_name(self) -> str:
        for priority_code, priority_display_name in Task.PRIORITY_CHOICES:
            if priority_code == self.priority:
                return priority_display_name

    @property
    def deadline_expired(self) -> bool:
        return self.deadline < datetime.now(tz=timezone(settings.TIME_ZONE))

    def __str__(self) -> str:
        return f"{self.name}, created at {self.created_at} (deadline {self.deadline})"
