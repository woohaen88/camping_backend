from ninja import ModelSchema
from campgrounds.models import Campground


class ALLCampgroundSchema(ModelSchema):
    class Config:
        model = Campground
        model_fields = "__all__"
