from typing import List

from ninja import ModelSchema, Schema, Field
from campgrounds.models import Campground, Amenity, Image, Review
from django.contrib.auth import get_user_model


class MessageSchema(Schema):
    message: str


class TinyUserSchema(ModelSchema):
    class Config:
        model = get_user_model()
        model_fields = [
            "id",
            "email",
            "username",
            "avatar",
            "first_name",
            "last_name",
        ]


class ImageSchema(ModelSchema):
    class Config:
        model = Image
        model_fields = ["id", "file"]


class AmenitySchema(ModelSchema):
    class Config:
        model = Amenity
        model_fields = ["id", "name"]


class ReviewSchema(ModelSchema):
    owner: TinyUserSchema

    class Config:
        model = Review
        model_fields = [
            "id",
            "content",
            "owner",
            "campground",
            "created_at",
            "updated_at",
        ]


class ALLCampgroundSchema(ModelSchema):
    owner: TinyUserSchema
    amenities: List[AmenitySchema] = []
    images: List[ImageSchema] = Field(None, alias="images")
    reviews: List[ReviewSchema] = Field(None, alias="reviews")

    class Config:
        model = Campground
        model_fields = "__all__"


class TinyCampgroundSchema(ModelSchema):
    owner: TinyUserSchema
    images: List[ImageSchema] = Field(None, alias="images")

    class Config:
        model = Campground
        model_fields = [
            "id",
            "name",
            "rating",
            "price",
            "location",
            "visited_at",
            "visited_end",
            "view",
            "owner",
        ]
