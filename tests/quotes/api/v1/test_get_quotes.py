import pytest
from django.urls import reverse

from apps.quotes.libs.alpha_vantage_client import AlphaVantageClient
from apps.quotes.models import Quote
from tests.fixtures.api_client.client import ApiClient

pytestmark = pytest.mark.django_db


class TestGetQuotesView:
    @pytest.fixture
    def quotes(self):
        quotes_data = [
            ("BTC/EUR", "37756.82640000"),
            ("BTC/USD", "43101.40000000"),
            ("BTC/AED", "158365.71481500"),
            ("BTC/USD", "43101.40000000"),
            ("BTC/EUR", "37752.38508000"),
            ("BTC/AED", "158377.17426300"),
            ("BTC/USD", "43101.40000000"),
            ("BTC/EUR", "37752.38508000"),
            ("BTC/AED", "158364.24565500"),
        ]

        for x in quotes_data:
            Quote.objects.create(pair_code=x[0], pair_price=x[1])

    def test_get_quotes_ok(self, quotes, auth_api_client: ApiClient):
        # Create most recent Quotes.
        Quote.objects.create(
            pair_code="BTC/USD",
            pair_price="43189.99000000",
        )
        Quote.objects.create(
            pair_code="BTC/EUR",
            pair_price="37833.46764000",
        )

        result = auth_api_client.get(reverse("quotes:get_quotes"))

        assert result.status_code == 200
        data = result.json()
        assert data == {"BTC/USD": "43189.99000000", "BTC/EUR": "37833.46764000"}

    def test_post_quotes_ok(self, quotes, mocker, auth_api_client: ApiClient):
        mocker.patch.object(
            AlphaVantageClient,
            "retrieve_exchange_rates",
            return_value={"BTC/USD": "43189.99000000", "BTC/EUR": "37833.46764000"},
            autospec=True,
        )

        result = auth_api_client.post(reverse("quotes:get_quotes"))

        assert result.status_code == 200
        data = result.json()
        assert data == {"BTC/USD": "43189.99000000", "BTC/EUR": "37833.46764000"}

    def test_get_quotes_anon(self, anon_api_client: ApiClient):
        result = anon_api_client.get(reverse("quotes:get_quotes"))
        assert result.status_code == 401
        data = result.json()
        assert data == {"detail": "Authentication credentials were not provided."}

    def test_post_quotes_anon(self, anon_api_client: ApiClient):
        result = anon_api_client.post(reverse("quotes:get_quotes"))
        assert result.status_code == 401
        data = result.json()
        assert data == {"detail": "Authentication credentials were not provided."}
