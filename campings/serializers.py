from rest_framework import serializers

from campings.models import CampGround
from users.serializers import TinyUserSerializer


class CampGroundSerializer(serializers.ModelSerializer):
    owner = TinyUserSerializer(read_only=True)

    class Meta:
        model = CampGround
        fields = [
            "name",
            "owner",
            "address",
            "check_in",
            "check_out",
            "ratings",
            "description",
            "created_at",
            "updated_at",
        ]

    def validate(self, value):
        check_in = value["check_in"]
        return value
