from typing import Tuple

from celery import shared_task

from apps.quotes.services import update_quotes


@shared_task(
    name="quotes.update_quotes_task",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 10},
)
def update_quotes_task(self, pairs_to_update: Tuple[Tuple[str, str], ...]) -> None:
    update_quotes(pairs_to_update=pairs_to_update)
