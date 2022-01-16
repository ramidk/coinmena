from typing import List

from django.conf import settings
from django.db.models import Max
from django.http import JsonResponse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.views import APIView

from apps.quotes.libs.utils import build_pair_code
from apps.quotes.models import Quote
from apps.quotes.services import update_quotes


class GetQuotesView(APIView):
    http_method_names = ["post", "get"]

    def get(self, request: Request) -> JsonResponse:
        pairs = settings.ALPHAVANTAGE_LOAD_CURRENCY_EXCHANGE_RATE_PAIRS
        pairs_formatted = [build_pair_code(from_cur=x[0], to_cur=x[1]) for x in pairs]

        # Should we return stale data in case update_quotes celery task fails?
        # let's assume that stale data is OK.

        qs = Quote.objects.all()

        latest_created_dt = qs.values("pair_code").annotate(
            latest_created_dt=Max("created_dt")
        )
        quotes = qs.filter(
            created_dt__in=latest_created_dt.values("latest_created_dt"),
            pair_code__in=pairs_formatted,
        )

        # In case no quotes exists in DB yet will return empty result.

        return JsonResponse(
            {x.pair_code: x.pair_price for x in quotes}, status=status.HTTP_200_OK
        )

    def post(self, request: Request) -> JsonResponse:
        pairs_to_update = settings.ALPHAVANTAGE_LOAD_CURRENCY_EXCHANGE_RATE_PAIRS
        quotes: List[Quote] = update_quotes(pairs_to_update=pairs_to_update)

        return JsonResponse(
            {x.pair_code: x.pair_price for x in quotes}, status=status.HTTP_200_OK
        )
