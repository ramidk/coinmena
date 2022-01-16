import pytest

from apps.quotes.libs.alpha_vantage_client import AlphaVantageClient


class TestAlphaVantageClient:
    """
    Actually calls alphavantage API for integration testing.
    """

    @pytest.fixture
    def av(self):
        return AlphaVantageClient()

    def test_retrieve_exchange_rates(self, av: AlphaVantageClient):
        pairs_to_retrieve = (("BTC", "USD"), ("BTC", "EUR"))

        data = av.retrieve_exchange_rates(pairs=pairs_to_retrieve)
        print(data)
        assert len(data.keys()) == 2
        assert data["BTC/USD"]
        assert data["BTC/EUR"]

    def test_retrieve_exchange_rate(self, av: AlphaVantageClient):
        pair_code, pair_price = av.retrieve_exchange_rate(from_cur="BTC", to_cur="USD")
        assert pair_code == "BTC/USD"
        assert pair_price
