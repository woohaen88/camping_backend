from ninja import Router
from campgrounds.schema import (
    ALLCampgroundSchema,
    TinyCampgroundSchema,
    MessageSchema,
    UpdateCampgroundSchema,
    CreateCampgroundSchema,
    OneTimeUploadSchema,
    CampgroundUploadSchemaIn,
    CampgroundUploadSchemaOut,
)
from typing import List
from ninja.responses import codes_4xx, codes_2xx
from django.shortcuts import get_object_or_404
from ninja.errors import ValidationError

# custom
from campgrounds.models import Campground
from ninja.security import django_auth
from django.conf import settings
from ninja.errors import HttpError
from campgrounds.models import Image

import requests

router = Router(tags=["Camping"])


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
    ["PUT", "PATCH"],
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


@router.post(
    "/",
    response={
        200: ALLCampgroundSchema,
        codes_4xx: MessageSchema,
    },
    auth=django_auth,
)
def create_campground(request, payload: CreateCampgroundSchema):
    payload_dict = payload.dict()

    try:
        campground = Campground.objects.create(owner=request.user, **payload_dict)
    except Exception:
        return 400, ValidationError("저기여 잘못됐어요")
    return 200, campground


# media
# {'id': '5a9589f9-a4d5-44a8-178d-80380a1bc600', 'uploadURL': 'https://upload.imagedelivery.net/4Rif_N_iuDtYv_8KyNzDpg/5a9589f9-a4d5-44a8-178d-80380a1bc600'
@router.post(
    "/image/one-time-upload",
    response={200: OneTimeUploadSchema, codes_4xx: MessageSchema},
)
def get_onetime_url(request):
    url = f"https://api.cloudflare.com/client/v4/accounts/{settings.CF_ID}/images/v2/direct_upload"
    try:
        one_time_url = requests.post(
            url, headers={"Authorization": f"Bearer {settings.CF_TOKEN}"}
        )
    except Exception:
        return 400, {"message": "bad request!"}
    one_time_url = one_time_url.json()

    result = one_time_url.get("result")
    id = result.get("id")
    uploadURL = result.get("uploadURL")

    return 200, {
        "id": id,
        "uploadURL": uploadURL,
    }


# /campgrounds/1/image/upload
# {
#     file: URLField
# }
@router.post(
    "/{campground_id}/image/upload",
    response={200: CampgroundUploadSchemaOut},
    auth=django_auth,
)
def campground_image_upload(
    request, campground_id: int, payload: CampgroundUploadSchemaIn
):
    payload_dict = payload.dict()
    file = payload_dict.get("file")

    try:
        campground = Campground.objects.get(id=campground_id)
    except Exception:
        raise HttpError(404, "저기여 데이터가 없어영!!")

    Image.objects.create(
        file=file,
        owner=request.user,
        campground=campground,
    )

    return 200, {"message": "이미지 업로드 성공"}
