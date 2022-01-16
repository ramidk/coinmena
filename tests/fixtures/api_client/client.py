from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


def create_token(user: User) -> Token:
    return Token.objects.create(user=user)


class ApiClient(APIClient):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", AnonymousUser())

        if not self.user.is_anonymous:
            self.token = create_token(user=self.user)

        super().__init__(*args, **kwargs)

    def _base_environ(self, **request):
        environ = super()._base_environ(**request)

        if not self.user.is_anonymous:
            environ["HTTP_AUTHORIZATION"] = f"Token {self.token}"

        return environ
