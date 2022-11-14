from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=63)

    def __str__(self) -> str:
        return self.name

class Task(models.Model):
    STATUS_CHOICES = (
        ("Done", "Done"),
        ("Not done", "Not done"),
    )

    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    status = models.CharField(
        max_length=63, choices=STATUS_CHOICES, default="Not done"
    )
    tags = models.ManyToManyField("Tag", related_name="task")
