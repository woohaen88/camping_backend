from ninja import Router
from campgrounds.schema import ALLCampgroundSchema
from typing import List
from django.http import HttpResponse

# custom
from campgrounds.models import Campground

router = Router(tags=["Camping"])


# @router.get("/", deprecated=True)
# def hello_world(request):
#     return {"message": "hello_world"}


@router.get("/", response=List[ALLCampgroundSchema])
def get_all_campgrounds(request, response: HttpResponse):
    # response["Access-Control-Allow-Origin"] = "User-Agent"

    return Campground.objects.all()


#   res.header("Access-Control-Allow-Origin", "*");
