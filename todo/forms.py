from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.forms import HiddenInput

from todo.models import Task, Tag


class TagForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    class Meta:
        model = Tag
        fields = ["name"]

    def clean_name(self):
        name = self.cleaned_data["name"]

        if Tag.objects.filter(Q(user_id=self.user.id) & Q(name=name)).exists():
            raise ValidationError("This tag already represented in your list")

        return self.cleaned_data["name"]


class TagSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}),
    )


class TaskForm(forms.ModelForm):
    class DateTimeInput(forms.DateTimeInput):
        input_type = "datetime-local"

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

        self.fields["deadline"].widget = TaskForm.DateTimeInput()

        self.fields["description"].required = False

        self.fields["tags"].required = False
        self.fields["tags"].queryset = Tag.objects.filter(user_id=user.id)

    class Meta:
        model = Task
        fields = ["name", "description", "deadline", "priority", "tags"]


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}),
    )
