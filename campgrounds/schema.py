from typing import List

from ninja import ModelSchema, Schema, Field
from campgrounds.models import Campground, Amenity, Image, Review
from django.contrib.auth import get_user_model
from users.shcema import TinyUserSchema


class MessageSchema(Schema):
    message: str


class ImageSchema(ModelSchema):
    class Config:
        model = Image
        model_fields = ["id", "file"]


class AmenitySchema(ModelSchema):
    class Config:
        model = Amenity
        model_fields = ["id", "name"]


class UpdateAmenitySchema(ModelSchema):
    class Config:
        model = Amenity
        model_fields = ["name"]


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


# campground schema
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


class UpdateCampgroundSchema(ModelSchema):
    class Config:
        model = Campground
        model_exclude = ["owner", "created_at", "updated_at", "amenities", "id"]
        model_fields_optional = "__all__"


class CreateCampgroundSchema(ModelSchema):
    class Config:
        model = Campground
        model_fields = [
            "name",
            "rating",
            "price",
            "view",
            "visited_at",
            "visited_end",
            "manner_time_start",
            "manner_time_end",
            "content",
            "maximum_people",
            "is_ev_charge",
            "camping_kind",
            "location",
            "location_lat_lon",
        ]


class OneTimeUploadSchema(Schema):
    id: str
    uploadURL: str


# Image
class CampgroundUploadSchemaIn(ModelSchema):
    class Config:
        model = Image
        model_fields = [
            "file",
        ]


class CampgroundUploadSchemaOut(Schema):
    message: str


# search
class CampgroundSearchSchema(Schema):
    search: str
