from django.urls import path

from .api.v1.get_quotes_view import GetQuotesView

urlpatterns = [
    path("", GetQuotesView.as_view(), name="get_quotes"),
]
