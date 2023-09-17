from ninja import Router
from campgrounds.schema import ALLCampgroundSchema, TinyCampgroundSchema, MessageSchema
from typing import List
from django.http import HttpResponse
from ninja.responses import codes_4xx

# custom
from campgrounds.models import Campground

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
