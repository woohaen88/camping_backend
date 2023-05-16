from rest_framework import serializers
from django.contrib.auth import (
    get_user_model,
    authenticate,
    login,
)


class TinyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "is_superuser",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "is_active",
        ]


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password1 = serializers.CharField(max_length=255)
    password2 = serializers.CharField(max_length=255)
    username = serializers.CharField(
        max_length=255,
        allow_blank=True,
        allow_null=True,
    )

    class Meta:
        model = get_user_model()
        fields = [
            "email",
            "password1",
            "password2",
            "username",
        ]


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get("email", None)
        password = attrs.get("password", None)

        assert email is not None and password is not None, "email이나 password값이 없음."

        return attrs


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "email",
            "avatar",
            "username",
            "is_superuser",
            "first_name",
            "last_name",
            "is_staff",
        ]
