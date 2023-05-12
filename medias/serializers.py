from rest_framework import serializers

from medias.models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    # file = serializers.ImageField()

    class Meta:
        model = Photo
        fields = [
            "id",
            "owner",
            "file",
            "description",
        ]
        extra_kwargs = {"owner": {"read_only": True}}

    def validate_file(self, value):
        return value

    def create(self, validated_data):
        print("validated_data: ", validated_data)
