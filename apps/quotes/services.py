from typing import Dict
from typing import List
from typing import Tuple

from apps.quotes.libs.alpha_vantage_client import AlphaVantageClient
from apps.quotes.models import Quote


def update_quotes(pairs_to_update: Tuple[Tuple[str, str], ...]) -> List[Quote]:
    av = AlphaVantageClient()

    pairs: Dict[str, str] = av.retrieve_exchange_rates(pairs=pairs_to_update)

    quotes = []
    for pair, price in pairs.items():
        quotes.append(Quote(pair_code=pair, pair_price=price))

    result = Quote.objects.bulk_create(quotes)

    return result
