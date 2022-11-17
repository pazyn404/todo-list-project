from django import forms

from todo.models import Task


class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"


class TaskForm(forms.ModelForm):
    deadline = forms.DateTimeField(widget=DateTimeInput)

    class Meta:
        model = Task
        fields = ["name", "deadline", "tags"]
