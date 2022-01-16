import pytest
from django.urls import reverse

from tests.fixtures.api_client.client import ApiClient

pytestmark = pytest.mark.django_db


class TestLogoutUserView:
    def test_logout_user_ok(self, auth_api_client: ApiClient):
        result = auth_api_client.post(reverse("auth:logout_user"))

        assert result.status_code == 204
        assert not result.content

        # check when called twice
        result = auth_api_client.post(reverse("auth:logout_user"))

        assert result.status_code == 401
        data = result.json()
        assert data == {"detail": "Invalid token."}

    def test_anon_user_fails_logout(self, anon_api_client: ApiClient):
        result = anon_api_client.post(reverse("auth:logout_user"))

        assert result.status_code == 401
        data = result.json()
        assert data == {"detail": "Authentication credentials were not provided."}
