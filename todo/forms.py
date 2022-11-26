from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q

from todo.models import Task, Tag


class TagForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

        if self.instance.id is not None:
            self.fields["name"].value = self.instance.name

    class Meta:
        model = Tag
        fields = ["name"]

    def clean_name(self):
        name = self.cleaned_data["name"]

        if Tag.objects.filter(Q(user_id=self.user.id) & Q(name=name)).exists():
            raise ValidationError(
                "This tag is already represented in your list!"
            )

        return name


class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

        self.fields["tags"].queryset = Tag.objects.filter(user_id=user.id)

        self.fields["tags"].required = False
        self.fields["description"].required = False

        self.fields["priority"].choices = Task.PRIORITY_CHOICES

        if self.instance.id is not None:
            self.fields["name"].value = self.instance.name
            self.fields["deadline"].value = self.instance.deadline.strftime(
                "%Y-%m-%dT%H:%M"
            )
            self.fields["description"].value = self.instance.description
            self.fields["priority"].value = self.instance.priority
            self.fields["tags"].values = {
                tag.id: tag for tag in self.instance.tags.all()
            }

    class Meta:
        model = Task
        fields = ["name", "description", "deadline", "priority", "tags"]
