from ninja import Router
from campgrounds.schema import (
    ALLCampgroundSchema,
    TinyCampgroundSchema,
    MessageSchema,
    UpdateCampgroundSchema,
    UpdateAmenitySchema,
)
from typing import List
from ninja.responses import codes_4xx, codes_2xx
from django.shortcuts import get_object_or_404

# custom
from campgrounds.models import Campground, Amenity

router = Router(tags=["Camping"])


# @router.get("/", deprecated=True)
# def hello_world(request):
#     return {"message": "hello_world"}

# api/vi1/campgrounds


@router.get("/", response=List[TinyCampgroundSchema])
def get_all_campgrounds(request):
    return Campground.objects.all()


@router.get(
    "/{campground_id}",
    response={200: ALLCampgroundSchema, codes_4xx: MessageSchema},
)
def get_campgound_detail(request, campground_id: int):
    try:
        campground = Campground.objects.get(id=campground_id)
    except Campground.DoesNotExist:
        return 404, {"message": "저기여 없어요!!"}

    return campground


@router.delete(
    "/{campground_id}",
    response={200: MessageSchema, codes_4xx: MessageSchema},
)
def delete_campground_detail(request, campground_id: int):
    try:
        campground = Campground.objects.get(id=campground_id)
    except Campground.DoesNotExist:
        return 404, {"message": "저기여 없어요!!"}

    campground.delete()
    return 200, {"meesage": "삭제완!"}


@router.api_operation(
    ["PUT", "PATCh"],
    "/{campground_id}",
    response={
        200: ALLCampgroundSchema,
        codes_4xx: MessageSchema,
    },
)
def update_campground(request, campground_id: int, payload: UpdateCampgroundSchema):
    payload_dict = payload.dict()

    try:
        campground = Campground.objects.get(id=campground_id)
    except Campground.DoesNotExist:
        return 404, {"message": "저기여 없어요!!"}

    for key, value in payload_dict.items():
        if value:
            setattr(campground, key, value)
    campground.save()
    return 200, campground


@router.put(
    "/api/v1/campgrounds/amenities/{amenity_id}",
    response={codes_2xx: MessageSchema},
    tags=["amenities"],
)
def update_amenities(request, amenity_id: int, payload: UpdateAmenitySchema):
    amenity = get_object_or_404(Amenity, id=amenity_id)
    for key, value in payload.dict().items():
        if value:
            setattr(amenity, key, value)
    amenity.save()
    return 200, {"message": "성공!!"}


@router.delete(
    "/api/v1/campgrounds/amenities/{amenity_id}",
    response={codes_2xx: MessageSchema},
    tags=["amenities"],
)
def delte_amenities(request, amenity_id: int, payload: UpdateAmenitySchema):
    amenity = get_object_or_404(Amenity, id=amenity_id)

    amenity.delete()
    return 200, {"message": "성공!!"}
