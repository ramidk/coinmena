import pytest
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User

from tests.fixtures.api_client.client import ApiClient


def user_factory(username: str = None, password: str = None) -> User:
    username = username or "default_user"
    password = password or "default_user"

    user = User(username=username)
    user.set_password(raw_password=password)
    user.save()

    return user


@pytest.fixture
def user():
    return user_factory()


@pytest.fixture
def auth_api_client(user):
    return ApiClient(user=user)


@pytest.fixture
def anon_api_client():
    return ApiClient(user=AnonymousUser())
