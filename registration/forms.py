from django.contrib.auth.forms import UserCreationForm
from registration.models import User


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name")
