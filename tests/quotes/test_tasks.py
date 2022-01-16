from django.test import override_settings

from apps.quotes.tasks import update_quotes_task


class TestUpdateQuotes:
    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_update_quotes_task(self, mocker):
        mock_update_quotes = mocker.patch(
            "apps.quotes.tasks.update_quotes", return_value=None, autospec=True
        )

        update_quotes_task.delay(pairs_to_update=(("BTC", "USD"), ("BTC", "EUR")))

        assert update_quotes_task.name == "quotes.update_quotes_task"

        mock_update_quotes.assert_called_once_with(
            pairs_to_update=[["BTC", "USD"], ["BTC", "EUR"]]
        )
