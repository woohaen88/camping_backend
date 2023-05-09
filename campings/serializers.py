from rest_framework import serializers

from campings.models import CampGround
from users.serializers import TinyUserSerializer
from tags.serializers import TagSerializer


class CampGroundSerializer(serializers.ModelSerializer):
    owner = TinyUserSerializer(read_only=True)
    tags = TagSerializer(read_only=True)

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
            "tags",
        ]

    def validate(self, attrs):
        check_in = attrs.get("check_in", None)
        check_out = attrs.get("check_out", None)

        if check_in is not None and check_out is not None:
            if check_in >= check_out:
                raise serializers.ValidationError("체크인날짜는 체크아웃날짜보다 빠를수없습니다.")
        return attrs

    def create(self, validated_data):
        print("validated_data", validated_data)
