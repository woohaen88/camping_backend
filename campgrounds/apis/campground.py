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
    CampgroundSearchSchema,
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


def get_onetime_url():
    url = f"https://api.cloudflare.com/client/v4/accounts/{settings.CF_ID}/images/v2/direct_upload"
    try:
        one_time_url = requests.post(
            url, headers={"Authorization": f"Bearer {settings.CF_TOKEN}"}
        )
    except Exception as e:
        raise ValidationError(e)

    one_time_url = one_time_url.json()

    result = one_time_url.get("result")
    id = result.get("id")
    uploadURL = result.get("uploadURL")

    return {
        "id": id,
        "uploadURL": uploadURL,
    }


@router.post("/{campground_id}/image/upload")
def get_upload_url(request, campground_id: int):
    files = request.FILES
    file_list = files.getlist("file")

    for file in file_list:
        one_time_resp = get_onetime_url()  # id, uploadURL
        uploadURL = one_time_resp.get("uploadURL")

        uploaded_data_resp = requests.post(
            uploadURL,
            files={"file": file},
        )

        uploaded_data_resp = uploaded_data_resp.json()
        result = uploaded_data_resp.get("result")
        image_url = result.get("variants")[0]

        # camping object
        try:
            campground = Campground.objects.get(id=campground_id)
        except Exception:
            raise HttpError(404, "캠핑이 없어요!!!")

        Image.objects.create(owner=request.user, campground=campground, file=image_url)
    return 200, {"message": "업로드 성공!"}


@router.get("/search", response=List[ALLCampgroundSchema])
def search_campground(request, search: CampgroundSearchSchema):
    campground = Campground.objects.filter(search=search)
    return campground
