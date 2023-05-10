from rest_framework import serializers
from django.contrib.auth import get_user_model


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
