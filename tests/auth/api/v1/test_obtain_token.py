import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from tests.fixtures.api_client.client import ApiClient
from tests.fixtures.api_client.users import user_factory

pytestmark = pytest.mark.django_db


class TestObtainTokenView:
    TEST_USERNAME = "user1"
    TEST_PASSWORD = "user1pass"

    @pytest.fixture
    def user(self):
        return user_factory(username=self.TEST_USERNAME, password=self.TEST_PASSWORD)

    def test_obtain_token_ok(self, user: User, anon_api_client: ApiClient):
        payload = {
            "username": self.TEST_USERNAME,
            "password": self.TEST_PASSWORD,
        }
        result = anon_api_client.post(reverse("auth:obtain_auth_token"), data=payload)

        assert result.status_code == 200
        data = result.json()
        assert "token" in data

    def test_wrong_password(self, user: User, anon_api_client: ApiClient):
        payload = {
            "username": "wrong_pass",
            "password": self.TEST_PASSWORD,
        }
        result = anon_api_client.post(reverse("auth:obtain_auth_token"), data=payload)

        assert result.status_code == 400
        data = result.json()
        assert data == {
            "non_field_errors": ["Unable to log in with provided credentials."]
        }

    def test_user_not_exists(self, anon_api_client: ApiClient):
        payload = {
            "username": self.TEST_USERNAME,
            "password": self.TEST_PASSWORD,
        }
        result = anon_api_client.post(reverse("auth:obtain_auth_token"), data=payload)

        assert result.status_code == 400
        data = result.json()
        assert data == {
            "non_field_errors": ["Unable to log in with provided credentials."]
        }
