import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from tests.fixtures.api_client.client import ApiClient
from tests.fixtures.api_client.users import user_factory

pytestmark = pytest.mark.django_db


class TestRegisterUserView:
    TEST_USERNAME = "user1"
    TEST_PASSWORD = "user1pass"

    @pytest.fixture
    def existing_user(self):
        return user_factory(username=self.TEST_USERNAME)

    def test_register_ok(self, anon_api_client: ApiClient):
        payload = {
            "username": self.TEST_USERNAME,
            "password": self.TEST_PASSWORD,
            "password2": self.TEST_PASSWORD,
        }
        result = anon_api_client.post(reverse("auth:register_user"), data=payload)

        assert result.status_code == 201
        data = result.json()
        assert data == {"username": self.TEST_USERNAME}

    def test_password_mismatch(self, anon_api_client: ApiClient):
        payload = {
            "username": self.TEST_USERNAME,
            "password": "wrong_pass",
            "password2": self.TEST_PASSWORD,
        }
        result = anon_api_client.post(reverse("auth:register_user"), data=payload)

        assert result.status_code == 400
        data = result.json()
        assert data == {"password": ["Password fields didn't match."]}

    def test_username_already_exist(
        self, existing_user: User, anon_api_client: ApiClient
    ):
        payload = {
            "username": self.TEST_USERNAME,
            "password": self.TEST_PASSWORD,
            "password2": self.TEST_PASSWORD,
        }
        result = anon_api_client.post(reverse("auth:register_user"), data=payload)

        assert result.status_code == 409
        data = result.json()
        assert data == {"username": ["User already exists."]}
