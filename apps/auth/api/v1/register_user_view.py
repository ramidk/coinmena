from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError
from django.http import JsonResponse
from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.views import APIView


class RegisterUserSlr(serializers.Serializer):
    username = serializers.CharField(required=True)

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs


class RegisterUserView(APIView):
    permission_classes = [AllowAny]
    http_method_names = ["post"]

    def post(self, request: Request) -> JsonResponse:
        slr = RegisterUserSlr(data=request.data)
        slr.is_valid(raise_exception=True)

        user = User(username=slr.validated_data["username"])
        user.set_password(slr.validated_data["password"])
        try:
            user.save()
        except IntegrityError:
            return JsonResponse(
                {"username": ["User already exists."]},
                status=status.HTTP_409_CONFLICT,
            )

        return JsonResponse({"username": user.username}, status=status.HTTP_201_CREATED)
