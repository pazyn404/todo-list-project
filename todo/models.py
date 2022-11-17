import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=63)

    def __str__(self) -> str:
        return self.name


class Task(models.Model):
    STATUS_CHOICES = (
        (True, "Done"),
        (False, "Not done"),
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    status = models.BooleanField(default=False, choices=STATUS_CHOICES)
    archived = models.BooleanField(default=False)
    tags = models.ManyToManyField("Tag", related_name="task")

    @property
    def status_display_name(self) -> str:
        for status_code, status_display_name in Task.STATUS_CHOICES:
            if status_code == self.status:
                return status_display_name

    def deadline_expired(self) -> bool:
        return self.deadline < datetime.datetime.now()

    def __str__(self) -> str:
        return f"{self.name}, created at {self.created_at} (deadline {self.deadline})"


class Scheduler(AbstractUser):
    tags = models.ManyToManyField("Tag", related_name="schedulers")
    tasks = models.ManyToManyField("Task", related_name="schedulers")

    def __str__(self) -> str:
        return f"{self.username}, email {self.email}"
