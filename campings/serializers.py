from django.db import transaction


from rest_framework import serializers
from rest_framework.exceptions import ParseError, NotFound

from campings.models import CampGround
from medias.models import Photo
from medias.serializers import PhotoSerializer
from tags.models import Tag
from users.serializers import TinyUserSerializer
from tags.serializers import TagSerializer


class CampGroundListSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(
        many=True,
        required=False,
        # read_only=True,
    )
    tags = TagSerializer(
        read_only=True,
        many=True,
        required=False,
    )

    class Meta:
        model = CampGround
        fields = [
            "id",
            "name",
            "address",
            "price",
            "tags",
            "photos",
            "owner",
        ]


class CampGroundDetailSerializer(CampGroundListSerializer):
    owner = TinyUserSerializer(read_only=True)

    class Meta(CampGroundListSerializer.Meta):
        fields = CampGroundListSerializer.Meta.fields + [
            "check_in",
            "check_out",
            "ratings",
            "description",
            "created_at",
            "updated_at",
            "pet_friendly",
            "ev_friendly",
        ]

    def validate(self, attrs):
        check_in = attrs.get("check_in", None)
        check_out = attrs.get("check_out", None)

        if check_in is not None and check_out is not None:
            if check_in >= check_out:
                raise serializers.ValidationError("체크인날짜는 체크아웃날짜보다 빠를수없습니다.")
        return attrs

    def create(self, validated_data):
        tags = validated_data.pop("tags", None)
        if tags:
            try:
                with transaction.atomic():
                    campground = CampGround.objects.create(**validated_data)

                    for tag_id in tags:
                        try:
                            tag_obj = Tag.objects.get(id=tag_id)
                            campground.tags.add(tag_obj)

                            campground.save()

                        except Tag.DoesNotExist:
                            raise NotFound("Content가 없습니다.")

            except Exception as e:
                raise ParseError("bad request!!")

            return campground

        return CampGround.objects.create(**validated_data)

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags", None)
        files = validated_data.pop("files", None)
        if tags is not None:  # tags 값이 존재하면
            try:
                with transaction.atomic():
                    for tag_id in tags:
                        try:
                            tag_obj = Tag.objects.get(id=tag_id)
                            instance.tags.add(tag_obj)
                            instance.save()

                        except Tag.DoesNotExist:
                            raise NotFound("Content가 없습니다.")

            except Exception as e:
                raise ParseError("bad request!!")

        if files:
            files = files.getlist("files")

            for file in files:
                Photo.objects.create(
                    owner=self.context["request"].user,
                    campgrounds=instance,
                    file=file,
                )

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        return instance
