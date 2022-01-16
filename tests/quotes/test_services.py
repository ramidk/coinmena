import pytest

from apps.quotes.libs.alpha_vantage_client import AlphaVantageClient
from apps.quotes.models import Quote
from apps.quotes.services import update_quotes

pytestmark = pytest.mark.django_db


class TestUpdateQuotes:
    def test_update_quotes(self, mocker):
        mocker.patch.object(
            AlphaVantageClient,
            "retrieve_exchange_rates",
            return_value={"BTC/USD": "43189.99000000", "BTC/EUR": "37833.46764000"},
            autospec=True,
        )

        assert Quote.objects.count() == 0

        data = update_quotes(pairs_to_update=(("BTC", "USD"), ("BTC", "EUR")))

        assert Quote.objects.count() == 2
        assert len(data) == 2
        assert all([isinstance(x, Quote) for x in data])

        assert Quote.objects.filter(
            pair_code="BTC/USD", pair_price="43189.99000000"
        ).exists()

        assert Quote.objects.filter(
            pair_code="BTC/EUR", pair_price="37833.46764000"
        ).exists()
