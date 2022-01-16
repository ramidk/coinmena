import concurrent.futures
from typing import Dict
from typing import Tuple

from alpha_vantage.foreignexchange import ForeignExchange
from django.conf import settings

from apps.quotes.libs.utils import build_pair_code


class AlphaVantageClient:
    fx = ForeignExchange(key=settings.ALPHAVANTAGE_API_KEY)

    def retrieve_exchange_rate(self, from_cur: str, to_cur: str) -> Tuple[str, str]:
        data, meta_data = self.fx.get_currency_exchange_rate(
            from_currency=from_cur, to_currency=to_cur
        )

        # make sure we store currency code that actually came from the api
        pair_code = build_pair_code(
            from_cur=data["1. From_Currency Code"], to_cur=data["3. To_Currency Code"]
        )
        pair_price = data["5. Exchange Rate"]

        assert data["7. Time Zone"] == "UTC"

        return pair_code, pair_price

    def retrieve_exchange_rates(
        self, pairs: Tuple[Tuple[str, str], ...]
    ) -> Dict[str, str]:
        retrieved_pairs = {}

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            tasks = []

            for from_cur, to_cur in pairs:
                task = executor.submit(
                    self.retrieve_exchange_rate, from_cur=from_cur, to_cur=to_cur
                )
                tasks.append(task)

            for task in concurrent.futures.as_completed(tasks):
                pair_code, pair_price = task.result()
                retrieved_pairs[pair_code] = pair_price

        return retrieved_pairs
