from django.http import JsonResponse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.views import APIView


class LogoutUserView(APIView):
    http_method_names = ["post"]

    def post(self, request: Request) -> JsonResponse:
        request.auth.delete()

        return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)
