# from ninja import Router
# from campgrounds.schema import (
#     ALLCampgroundSchema,
#     TinyCampgroundSchema,
#     MessageSchema,
#     UpdateCampgroundSchema,
#     UpdateAmenitySchema,
# )
# from typing import List
# from ninja.responses import codes_4xx, codes_2xx
# from django.shortcuts import get_object_or_404

# # custom
# from campgrounds.models import Campground, Amenity


# router = Router(tags=["Camping"])


# @router.put(
#     "/api/v1/campgrounds/amenities/{amenity_id}",
#     response={codes_2xx: MessageSchema},
#     tags=["amenities"],
# )
# def update_amenities(request, amenity_id: int, payload: UpdateAmenitySchema):
#     amenity = get_object_or_404(Amenity, id=amenity_id)
#     for key, value in payload.dict().items():
#         if value:
#             setattr(amenity, key, value)
#     amenity.save()
#     return 200, {"message": "성공!!"}


# @router.delete(
#     "/api/v1/campgrounds/amenities/{amenity_id}",
#     response={codes_2xx: MessageSchema},
#     tags=["amenities"],
# )
# def delte_amenities(request, amenity_id: int, payload: UpdateAmenitySchema):
#     amenity = get_object_or_404(Amenity, id=amenity_id)

#     amenity.delete()
#     return 200, {"message": "성공!!"}
