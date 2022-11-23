from django.http import Http404
from django.shortcuts import get_object_or_404

from registration.models import User


class UserVerifyUrlDataMixin:
    def get(self, request, *args, **kwargs):
        if get_object_or_404(User, pk=kwargs["pk"]).id != request.user.id:
            raise Http404()

        return super().get(request, *args, **kwargs)